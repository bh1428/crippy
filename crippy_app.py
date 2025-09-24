#!/usr/bin/env python3
"""Encrypt / decrypt text strings and files to BASE64 encoded blocks."""

import base64
import dataclasses
import pathlib
import re
import secrets
import zlib

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# default SALT (generate new salt using: "import secrets; secrets.token_hex(16)"
SALT = bytes.fromhex("e512060efc9b086e9951d505bab83173")


class InvalidBlockException(Exception):
    """No valid block markers found."""


class InvalidDataException(Exception):
    """Data to be processed is missing."""


class MissingFilenameException(Exception):
    """Missing filename a DataObject."""


class InvalidContentException(Exception):
    """Invalid Content-Type for operation."""


@dataclasses.dataclass
class DataObject:
    """Object to represent a piece of binary data (text or file content)."""

    DEFAULT_CHARSET = "utf-8"

    content_type: None | str = None
    charset: None | str = None
    is_zipped: bool = False
    filename: None | str = None
    binary_data: None | bytes = None

    def _store_data(self, data: bytes, zip_data: None | bool = None) -> None:
        """Store the binary data.

        Depending on the value of the `zip_data` argument the data may or may
        not be compressed:
          None: auto mode (default), data is compressed when it is compressible
          False: data will not be compressed
          True: data will be compressed

        Args:
            data (bytes): the data to be stored
            zip_data (None | bool, optional): compression mode
        """
        if data is not None:
            # zip when required
            if (zip_data is None) or (isinstance(zip_data, bool) and zip_data):
                zipped_data = zlib.compress(data)
                if zip_data is None:
                    # auto mode: decide if zipping makes sense
                    zip_data = bool(len(zipped_data) < len(data))
            # store either zipped or raw data
            if zip_data:
                self.binary_data = zipped_data
                self.is_zipped = True
            else:
                self.binary_data = data
                self.is_zipped = False

    @classmethod
    def from_str(cls, text: str, charset: None | str = None, zip_data: None | bool = None) -> "DataObject":
        """Encode a string into a DataObject.

        If no `charset` is given the `DEFAULT_CHARSET` (utf-8) will be used.

        Depending on the value of the `zip_data` argument the data may or may
        not be compressed:
          None: auto mode (default), data is compressed when it is compressible
          False: data will not be compressed
          True: data will be compressed

        Args:
            text (str): text to be encoded as binary data
            charset (None | str, optional): charset to be used for encoding
            zip_data (None | bool, optional): compression mode

        Returns:
            DataObject: a new `DataObject`
        """
        # create and return a new DataObject from a string
        data_obj = cls()
        data_obj.content_type = "text/plain"
        data_obj.charset = data_obj.DEFAULT_CHARSET if charset is None else charset
        data_obj.filename = None
        if text is not None:
            data_obj._store_data(text.encode(data_obj.charset), zip_data)
        return data_obj

    def as_str(self, charset: None | str = None) -> None | str:
        """Get the binary content as text.

        If no `charset` is provided the `DEFAULT_CHARSET` will be used.

        Args:
            charset (None | str, optional): charset to be used for decoding

        Returns:
            None | str: binary content as string
        """
        if self.binary_data is not None:
            # make sure we always have a charset
            charset = self.charset if charset is None else charset
            charset = self.DEFAULT_CHARSET if charset is None else charset
            # return decoded data
            if self.is_zipped:
                return zlib.decompress(self.binary_data).decode(charset)
            return self.binary_data.decode(charset)
        return None

    @classmethod
    def from_file(cls, filename: str | pathlib.Path, zip_data: None | bool = None) -> "DataObject":
        """Load a file as a DataObject.

        Depending on the value of the `zip_data` argument the data may or may
        not be compressed:
          None: auto mode (default), data is compressed when it is compressible
          False: data will not be compressed
          True: data will be compressed

        Args:
            filename (str | pathlib.Path): file to be loaded
            zip_data (None | bool, optional): compression mode

        Returns:
            DataObject: a new `DataObject`
        """
        # create and return a new DataObject from a file
        data_obj = cls()
        data_obj.content_type = "application/octet-stream"
        filename = pathlib.Path(filename)
        data_obj.filename = filename.name
        data_obj.charset = None
        with open(filename, "rb") as fh_in:
            data = fh_in.read()
        data_obj._store_data(data, zip_data)
        return data_obj

    def to_file(
        self, filename: None | str | pathlib.Path = None, directory: None | str | pathlib.Path = None
    ) -> None | tuple[str, int]:
        """Write binary content to a file.

        There are a number of ways the name and location of the file to be
        written is determined:
          * the `filename` argument to this function is used when provided
          * in case no `filename` argument is provided used the `filename`
            attribute of the `DataObject`
          * still no filename found -> raise an `DataObjectException`

        With regard to the directory: the `directory` argument is only used
        when given (obviously) AND when the filename does not contain any
        directories. Default directory is always the current working
        directory.

        Args:
            filename (None | str | pathlib.Path, optional): filename
            directory (None | str | pathlib.Path, optional): directory

        Raises:
            MissingFilenameException: no filename is known (or received)

        Returns:
            None | tuple[str, int]: (filename, number_of_bytes_written)
        """
        # early exit when nothing to do
        if self.binary_data is None:
            return None

        # find a filename: argument overrules attribute
        if filename is None:
            if self.filename is None:
                raise MissingFilenameException("to_file(): no filename received")
            target_file = pathlib.Path(self.filename)
        else:
            target_file = pathlib.Path(filename)

        # add directory but only when the filename contains no directories
        if (len(target_file.parts) == 1) and (directory is not None):
            target_file = pathlib.Path(directory) / target_file

        # save binary content to file
        with open(target_file, "wb") as fh_out:
            if self.is_zipped:
                num_bytes = fh_out.write(zlib.decompress(self.binary_data))
            else:
                num_bytes = fh_out.write(self.binary_data)
        return str(target_file), num_bytes


class BlockCrypter(Fernet):
    """Encrypt / decrypt text or files from / to BASE64 encoded blocks.

    This class is basically a standard `cryptography.fernet.Fernet` class
    with some additional logic to encode / decode from / to BASE64 blocks.
    `Fernet` is an implementation of symmetric (also known as "secret key")
    authenticated cryptography.

    The input and output of this class are BASE64 encoded blocks. Example
    of a block encoded from a string:
        ===== START BLOCK =====
        Content-Type: text/plain; charset=utf-8
        Content-Disposition: inline

        gAAAAABjLCAYakmn8Y--wK5bIBM8iBul0_xAFceVp-gtiDx8DSuqtRw_lCHXBD4c5Q-eKR
        cxB1peXF5AbuIfsLTe2sqTbGsuHg==
        ===== END BLOCK =====

    Example of a block encoded from a file:
        ===== START BLOCK =====
        Content-Type: application/octet-stream
        Content-Disposition: attachment; filename="filename.txt"

        gAAAAABjLCkL0G6QXaftdznNXf_qPmg4L0HZkqryb9mikihzWKfCLhOJYZwc9W7wch6D3a
        UoDk8vxQl_9zWIpvipdzYT9u1Z5WeIZilOT_W5Bo0LNlr2DBE=
        ===== END BLOCK =====

    Content can be zipped, if that is the case an additional header will be added:
        Content-Encoding: gzip
    and the data will is compressed (using zlib / gzip).
    """

    @classmethod
    def generate_salt(cls, length: int = 32) -> bytes:
        """Generate a suitable salt with a certain length.

        Args:
            length (int, optional): Length (in bytes) of the generated salt,
                defaults to 32.

        Returns:
            bytes: salt which is `length` bytes of random data
        """
        return secrets.token_bytes(length)

    @classmethod
    def derive_key_from_password(cls, password: str, salt: bytes, iterations: int = 1_500_000) -> bytes:
        """Derive a key from a password using the `PBKDF2HMAC` function.

        When using the `PBKDF2HMAC` function to generate a key from a password
        a salt is needed to prevent rainbow table based attacks. The salt has
        to be stored in a retrievable location in order to derive the same key
        from the password in the future.

        The `iterations` count used should be adjusted to be as high as your
        server can tolerate. We use 1_500_000 iterations as default. This is
        based on what Django uses for V6.1 (as of 2025-09-24:
        https://github.com/django/django/blob/main/django/contrib/auth/hashers.py).
        This may or may not be good enough for your application: you decide.

        Args:
            password (str): password to derive key from
            salt (bytes): salt to be used
            iterations (int, optional): _description_. Defaults to 480000.

        Returns:
            bytes: key suitable to use for encryption / decryption using Fernet.
        """
        backend = default_backend()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations, backend=backend)
        return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

    def __init__(self, *args, **kwargs):
        self.default_width = kwargs.pop("width", 70)
        super().__init__(*args, **kwargs)
        self._start_block = "===== START BLOCK ====="
        self._end_block = "===== END BLOCK ====="
        self._block = (
            f"{self._start_block}\n"
            "Content-Type: {content_type}\n"
            "Content-Disposition: {content_disposition}\n"
            "{content_encoding}"
            "\n"
            "{data}\n"
            f"{self._end_block}\n"
        )

    def encrypt_to_block(self, data: DataObject, width: None | int = None) -> str:
        """Encrypt data to a BASE64 encoded block with header and footer.

        Args:
            data (bytes): binary data to be encrypted
            width (None | int, optional): output block width, default: 70 chars

        Raises:
            InvalidDataException: in case of errors with the data

        Returns:
            str: BASE64 encoded block with header and footer
        """
        # input checks
        if not isinstance(data, DataObject):
            raise InvalidDataException("got no DataObject")
        if data.binary_data is None:
            raise InvalidDataException("got no binary_data")
        if data.content_type is None:
            raise InvalidDataException("no content_type specified")

        # prepare output
        content_type = data.content_type.lower()
        if content_type == "text/plain":
            content_disposition = "inline"
            if data.charset is not None:
                content_type += f"; charset={data.charset.lower()}"
        elif content_type == "application/octet-stream":
            content_disposition = "attachment"
            if data.filename is not None:
                content_disposition += f'; filename="{data.filename}"'
        else:
            raise InvalidDataException(f"content_type '{data.content_type}' is not supported")
        content_encoding = "Content-Encoding: gzip\n" if data.is_zipped else ""

        # encrypt data
        encrypted_data = super().encrypt(data.binary_data).decode("ASCII")

        # generate output
        if width is None:
            width = self.default_width
        if width > 0:
            encrypted_data = "\n".join(encrypted_data[i : i + width] for i in range(0, len(encrypted_data), width))

        return self._block.format(
            content_type=content_type,
            content_disposition=content_disposition,
            content_encoding=content_encoding,
            data=encrypted_data,
        )

    def _create_dataobject(
        self, content_type: str, content_disposition: str, content_encoding: None | str, binary_data: bytes
    ) -> "DataObject":
        """Create a DataObject from a decrypted block.

        Args:
            content_type (str): "Content-Type:" in header
            content_disposition (str): "Content-Disposition:" in header
            content_encoding (None | str): "Content-Encoding:" in header
            binary_data (bytes): binary data to be stored

        Raises:
            InvalidContentException: content is in an unsupported format

        Returns:
            DataObject: new `DataObject` with data
        """
        # variables for creating a new DataObject
        obj_content_type = None
        obj_charset = None
        obj_is_zipped = False
        obj_filename = None

        # get content_type, charset and filename
        content_type_lower = content_type.lower()
        if "text/plain" in content_type_lower:
            obj_content_type = "text/plain"
            re_char_set = re.compile(r"\;\s*charset\s*\=\s*['\"]*(?P<charset>[^'\";\s]+)['\";\s]*", re.IGNORECASE)
            if mt_char_set := re_char_set.search(content_type_lower):
                obj_charset = mt_char_set["charset"].strip()
        elif "application/octet-stream" in content_type_lower:
            obj_content_type = "application/octet-stream"
            re_filename = re.compile(r"\;\s*filename\s*\=\s*['\"]*(?P<filename>[^'\";]+)['\";\s]*", re.IGNORECASE)
            if mt_filename := re_filename.search(content_disposition):
                obj_filename = mt_filename["filename"].strip()
        else:
            raise InvalidContentException(f"_create_dataobject(): content_type is not supported: '{content_type}'")

        # is the binary data zipped?
        if content_encoding is not None:
            if content_encoding.lower().strip() == "gzip":
                obj_is_zipped = True
            else:
                raise InvalidContentException(
                    f"_create_dataobject(): content_encoding is not supported: '{content_encoding}'"
                )

        return DataObject(
            content_type=obj_content_type,
            charset=obj_charset,
            is_zipped=obj_is_zipped,
            filename=obj_filename,
            binary_data=binary_data,
        )

    def decrypt_from_block(self, block: str) -> DataObject:
        """Decrypt a BASE64 encoded block with header and footer.

        Args:
            block (str): BASE64 encoded block with header and footer

        Raises:
            InvalidBlockException: error in block content

        Returns:
            DataObject: object containing decrypted information
        """
        # first find the block
        start_block_pos = block.find(self._start_block)
        end_block_pos = block.find(self._end_block)
        if (start_block_pos == -1) or (end_block_pos == -1):
            raise InvalidBlockException("cannot find block markers")
        start_block_pos += len(self._start_block)

        # get content type and disposition
        content_type = None
        content_disposition = None
        content_encoding = None
        base64_start_pos = start_block_pos
        for line in block[start_block_pos:end_block_pos].splitlines(keepends=True):
            if len(line.strip()) > 0:
                if ":" in line:
                    if match := re.match(r"^\s*content\-type\:\s*(?P<type>.*)\s*$", line, re.IGNORECASE):
                        content_type = match["type"]
                    elif match := re.match(r"^\s*content\-disposition\:\s*(?P<disp>.*)\s*$", line, re.IGNORECASE):
                        content_disposition = match["disp"]
                    elif match := re.match(r"^\s*content\-encoding\:\s*(?P<enc>.*)\s*$", line, re.IGNORECASE):
                        content_encoding = match["enc"]
                else:
                    # a non-empty line without ":" -> must be the start of the data
                    break
            base64_start_pos += len(line)
        if content_type is None:
            raise InvalidBlockException("expected 'Content-Type:' not found in block")
        if content_disposition is None:
            raise InvalidBlockException("expected 'Content-Disposition:' not found in block")

        # decrypt and prepare DataObject
        decrypted_data = super().decrypt(block[base64_start_pos:end_block_pos].replace("\n", "").encode("ASCII"))
        return self._create_dataobject(content_type, content_disposition, content_encoding, decrypted_data)
