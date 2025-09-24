#!/usr/bin/env python3
"""Unit tests for crippy_app.py"""

import base64
import inspect
import pathlib
import unittest
import unittest.mock as mk
import zlib

from crippy_app import (
    BlockCrypter,
    DataObject,
    InvalidBlockException,
    InvalidContentException,
    InvalidDataException,
    MissingFilenameException,
)

# pylint: disable=missing-class-docstring, missing-function-docstring, no-value-for-parameter, unused-argument
# pylint: disable=invalid-name, unnecessary-dunder-call, protected-access, too-many-public-methods
# pylint: disable=too-many-instance-attributes


class TestDataObject(unittest.TestCase):
    def test001_no_init_parameters_required(self):
        obj = DataObject()
        self.assertIsInstance(obj, DataObject)

    def test002_from_str_no_input(self):
        with self.assertRaises(TypeError):
            DataObject.from_str()

    def test003_from_str_none_as_input_no_zip(self):
        expected = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data=None,
        )
        obj = DataObject.from_str(None, zip_data=False)
        self.assertEqual(obj, expected)

    def test004_from_str_none_as_input_forced_zip(self):
        expected = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data=None,
        )
        obj = DataObject.from_str(None, zip_data=True)
        self.assertEqual(obj, expected)

    def test005_from_str_empty_str_as_input(self):
        expected = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data=b"",
        )
        obj = DataObject.from_str("", zip_data=False)
        self.assertEqual(obj, expected)

    def test006_from_str_str_as_input(self):
        text = inspect.currentframe().f_code.co_name  # method name
        expected = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data=text.encode("utf-8"),
        )
        obj = DataObject.from_str(text, zip_data=False)
        self.assertEqual(obj, expected)

    def test007_from_str_utf16_encoding(self):
        text = "test005"
        expected = DataObject(
            content_type="text/plain",
            charset="utf-16",
            is_zipped=False,
            filename=None,
            binary_data=text.encode("utf-16"),
        )
        obj = DataObject.from_str(text, charset="utf-16", zip_data=False)
        self.assertEqual(obj, expected)

    def test008_from_str_auto_zip_mode_no_zip(self):
        text = "t"
        expected = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data=text.encode("utf-8"),
        )
        obj = DataObject.from_str(text)
        self.assertEqual(len(obj.binary_data), len(text))
        self.assertEqual(obj, expected)

    def test009_from_str_auto_zip_mode_zip(self):
        text = "\n".join(inspect.currentframe().f_code.co_name * 1000)  # 1000 lines with method name
        expected = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=True,
            filename=None,
            binary_data=zlib.compress(text.encode("utf-8")),
        )
        obj = DataObject.from_str(text)
        self.assertNotEqual(len(obj.binary_data), len(text))
        self.assertEqual(obj, expected)

    def test010_from_str_no_zip(self):
        text = "\n".join(inspect.currentframe().f_code.co_name * 1000)  # 1000 lines with method name
        expected = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data=text.encode("utf-8"),
        )
        obj = DataObject.from_str(text, zip_data=False)
        self.assertEqual(len(obj.binary_data), len(text))
        self.assertEqual(obj, expected)

    def test011_from_str_utf16_encoding_forced_zip(self):
        text = "test011"
        expected = DataObject(
            content_type="text/plain",
            charset="utf-16",
            is_zipped=True,
            filename=None,
            binary_data=zlib.compress(text.encode("utf-16")),
        )
        obj = DataObject.from_str(text, charset="utf-16", zip_data=True)
        self.assertNotEqual(len(obj.binary_data), len(text))
        self.assertEqual(obj, expected)

    def test012_as_str_no_binary_data(self):
        obj = DataObject()
        self.assertIsNone(obj.as_str())

    def test013_as_str_default_charset(self):
        text = "test013"
        obj = DataObject(
            content_type="text/plain",
            charset=None,
            is_zipped=False,
            filename=None,
            binary_data=text.encode(DataObject.DEFAULT_CHARSET),
        )
        self.assertEqual(obj.as_str(), text)

    def test014_as_str_non_default_charset(self):
        text = "test014"
        obj = DataObject(
            content_type="text/plain",
            charset="utf-16",
            is_zipped=False,
            filename=None,
            binary_data=text.encode("utf-16"),
        )
        self.assertEqual(obj.as_str(), text)

    def test015_as_str_non_default_charset_as_argument(self):
        text = "test015"
        obj = DataObject(
            content_type="text/plain",
            charset=None,
            is_zipped=False,
            filename=None,
            binary_data=text.encode("utf-16"),
        )
        self.assertEqual(obj.as_str(charset="utf-16"), text)

    def test016_as_str_default_charset_zipped(self):
        text = "test016"
        obj = DataObject(
            content_type="text/plain",
            charset=None,
            is_zipped=True,
            filename=None,
            binary_data=zlib.compress(text.encode(DataObject.DEFAULT_CHARSET)),
        )
        self.assertEqual(obj.as_str(), text)

    def test017_as_str_non_default_charset(self):
        text = "test017"
        obj = DataObject(
            content_type="text/plain",
            charset="utf-16",
            is_zipped=True,
            filename=None,
            binary_data=zlib.compress(text.encode("utf-16")),
        )
        self.assertEqual(obj.as_str(), text)

    def test018_as_str_non_default_charset_as_argument(self):
        text = "test018"
        obj = DataObject(
            content_type="text/plain",
            charset=None,
            is_zipped=True,
            filename=None,
            binary_data=zlib.compress(text.encode("utf-16")),
        )
        self.assertEqual(obj.as_str(charset="utf-16"), text)

    def test019_from_file_no_input(self):
        with self.assertRaises(TypeError):
            DataObject.from_file()

    @mk.patch("crippy_app.open")
    def test020_from_file_none_as_file_content_no_zip(self, mk_open):
        data = None
        filename = inspect.currentframe().f_code.co_name
        expected = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=None,
        )
        mk_open.return_value.__enter__.return_value.read.return_value = data
        obj = DataObject.from_file(filename, zip_data=False)
        self.assertEqual(obj, expected)

    @mk.patch("crippy_app.open")
    def test021_from_file_none_as_file_content_forced_zip(self, mk_open):
        data = None
        filename = inspect.currentframe().f_code.co_name
        expected = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=None,
        )
        mk_open.return_value.__enter__.return_value.read.return_value = data
        obj = DataObject.from_file(filename, zip_data=True)
        self.assertEqual(obj, expected)

    @mk.patch("crippy_app.open")
    def test022_from_file_empty_file_as_input(self, mk_open):
        data = b""
        filename = inspect.currentframe().f_code.co_name
        expected = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=data,
        )
        mk_open.return_value.__enter__.return_value.read.return_value = data
        obj = DataObject.from_file(filename, zip_data=False)
        self.assertEqual(obj, expected)

    @mk.patch("crippy_app.open")
    def test023_from_file_no_zip(self, mk_open):
        data = "één test023".encode("utf-8")
        filename = inspect.currentframe().f_code.co_name
        expected = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=data,
        )
        mk_open.return_value.__enter__.return_value.read.return_value = data
        obj = DataObject.from_file(filename, zip_data=False)
        self.assertEqual(obj, expected)
        self.assertEqual(len(obj.binary_data), len(data))

    @mk.patch("crippy_app.open")
    def test024_from_file_with_content_forced_zip(self, mk_open):
        data = "één test024".encode("utf-8")
        filename = inspect.currentframe().f_code.co_name
        expected = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=True,
            filename=filename,
            binary_data=zlib.compress(data),
        )
        mk_open.return_value.__enter__.return_value.read.return_value = data
        obj = DataObject.from_file(filename, zip_data=True)
        self.assertEqual(obj, expected)
        self.assertNotEqual(len(obj.binary_data), len(data))

    @mk.patch("crippy_app.open")
    def test025_from_file_with_content_auto_zip_mode_no_zip(self, mk_open):
        data = "t".encode("utf-8")
        filename = inspect.currentframe().f_code.co_name
        expected = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=data,
        )
        mk_open.return_value.__enter__.return_value.read.return_value = data
        obj = DataObject.from_file(filename)
        self.assertEqual(obj, expected)
        self.assertEqual(len(obj.binary_data), len(data))

    @mk.patch("crippy_app.open")
    def test026_from_file_with_content_auto_zip_mode_zip(self, mk_open):
        data = "\n".join(inspect.currentframe().f_code.co_name * 1000).encode("utf-8")  # 1000 lines with method name
        filename = inspect.currentframe().f_code.co_name
        expected = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=True,
            filename=filename,
            binary_data=zlib.compress(data),
        )
        mk_open.return_value.__enter__.return_value.read.return_value = data
        obj = DataObject.from_file(filename)
        self.assertEqual(obj, expected)
        self.assertNotEqual(len(obj.binary_data), len(data))
        self.assertEqual(mk_open.mock_calls[0], mk.call(pathlib.WindowsPath(filename), "rb"))

    @mk.patch("crippy_app.open")
    def test027_to_file_no_data(self, mk_open):
        obj = DataObject()
        self.assertIsNone(obj.to_file())

    @mk.patch("crippy_app.open")
    def test028_to_file_filename_from_object(self, mk_open):
        filename = inspect.currentframe().f_code.co_name
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=b"",
        )
        obj.to_file()
        self.assertEqual(mk_open.mock_calls[0], mk.call(pathlib.WindowsPath(filename), "wb"))

    @mk.patch("crippy_app.open")
    def test029_to_file_filename_from_argument(self, mk_open):
        filename = inspect.currentframe().f_code.co_name
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=False,
            filename="not_used.txt",
            binary_data=b"",
        )
        obj.to_file(filename)
        self.assertEqual(mk_open.mock_calls[0], mk.call(pathlib.WindowsPath(filename), "wb"))

    @mk.patch("crippy_app.open")
    def test030_to_file_filename_missing_filename(self, mk_open):
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=False,
            filename=None,
            binary_data=b"",
        )
        with self.assertRaises(MissingFilenameException):
            obj.to_file()

    @mk.patch("crippy_app.open")
    def test031_to_file_filename_add_directory_from_argument(self, mk_open):
        filename = inspect.currentframe().f_code.co_name
        directory = pathlib.Path(r"C:\temp")
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=b"",
        )
        obj.to_file(directory=directory)
        self.assertEqual(mk_open.mock_calls[0], mk.call(directory / pathlib.WindowsPath(filename), "wb"))

    @mk.patch("crippy_app.open")
    def test032_to_file_filename_directory_not_used(self, mk_open):
        filename = rf"..\{inspect.currentframe().f_code.co_name}"
        directory = pathlib.Path(r"C:\temp")
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=False,
            filename="not_used.txt",
            binary_data=b"",
        )
        obj.to_file(filename=filename, directory=directory)
        self.assertEqual(mk_open.mock_calls[0], mk.call(pathlib.WindowsPath(filename), "wb"))

    @mk.patch("crippy_app.open")
    def test033_to_file_empty_content(self, mk_open):
        filename = inspect.currentframe().f_code.co_name
        data = b""
        expected = (filename, len(data))
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=data,
        )
        mk_open.return_value.__enter__.return_value.write.return_value = len(data)
        result = obj.to_file()
        self.assertEqual(result, expected)
        self.assertEqual(mk_open.mock_calls[2], mk.call().__enter__().write(data))

    @mk.patch("crippy_app.open")
    def test034_to_file_non_zipped_content(self, mk_open):
        filename = inspect.currentframe().f_code.co_name
        data = filename.upper().encode("utf-8")
        expected = (filename, len(data))
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=False,
            filename=filename,
            binary_data=data,
        )
        mk_open.return_value.__enter__.return_value.write.return_value = len(data)
        result = obj.to_file()
        self.assertEqual(result, expected)
        self.assertEqual(mk_open.mock_calls[2], mk.call().__enter__().write(data))

    @mk.patch("crippy_app.open")
    def test035_to_file_zipped_content(self, mk_open):
        filename = inspect.currentframe().f_code.co_name
        data = filename.upper().encode("utf-8")
        expected = (filename, len(data))
        obj = DataObject(
            content_type=None,
            charset=None,
            is_zipped=True,
            filename=filename,
            binary_data=zlib.compress(data),
        )
        mk_open.return_value.__enter__.return_value.write.return_value = len(data)
        result = obj.to_file()
        self.assertEqual(result, expected)
        self.assertEqual(mk_open.mock_calls[2], mk.call().__enter__().write(data))


class TestBlockCrypter(unittest.TestCase):
    PASSWORD = "secret"
    SALT = bytes.fromhex("df0eca086ba82a61fe76caaa6b9995ed")
    DERIVED_KEY_BIN = bytes.fromhex("9f4e34730ea696ce1d4029819171c8f50da30a78398a31b1aafce47321a2e2e4")
    DERIVED_KEY = base64.urlsafe_b64encode(DERIVED_KEY_BIN)

    def setUp(self):
        patch_fernet_init = mk.patch("crippy_app.Fernet.__init__", spec_set=True)
        self.addCleanup(patch_fernet_init.stop)
        self.mk_fernet_init = patch_fernet_init.start()
        patch_fernet_encrypt = mk.patch("crippy_app.Fernet.encrypt", spec_set=True)
        self.addCleanup(patch_fernet_encrypt.stop)
        self.mk_fernet_encrypt = patch_fernet_encrypt.start()
        patch_fernet_decrypt = mk.patch("crippy_app.Fernet.decrypt", spec_set=True)
        self.addCleanup(patch_fernet_decrypt.stop)
        self.mk_fernet_decrypt = patch_fernet_decrypt.start()
        self.data_object_str = DataObject(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data="dataobject: str".encode("utf-8"),
        )
        self.data_object_str_encrypted = (
            "gAAAAABjLCAYakmn8Y--wK5bIBM8iBul0_xAFceVp-gtiDx8DSuqtRw_lCHXBD4c5Q-eKRcxB1peXF5AbuIfsLTe2sqTbGsuHg=="
        ).encode("ASCII")
        self.data_object_str_block = (
            "===== START BLOCK =====\n"
            "Content-Type: text/plain; charset=utf-8\n"
            "Content-Disposition: inline\n"
            "\n"
            "gAAAAABjLCAYakmn8Y--wK5bIBM8iBul0_xAFceVp-gtiDx8DSuqtRw_lCHXBD4c5Q-eKR\n"
            "cxB1peXF5AbuIfsLTe2sqTbGsuHg==\n"
            "===== END BLOCK =====\n"
        )
        self.data_object_file = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=True,
            filename="filename.txt",
            binary_data=zlib.compress("dataobject: file".encode("utf-8")),
        )
        self.data_object_file_encrypted = (
            "gAAAAABjLCBfkrBO5yJLi1dybS3v_egUxC63Qkh7TkuJL64uasQ_H0APGTq5oJT94JVPx3"
            "_mlLvVbQISEXyPAKKbRtDesX9AxKMDxrSYMtKKOcLsAYPigCQ="
        ).encode("ASCII")
        self.data_object_file_block = (
            "===== START BLOCK =====\n"
            "Content-Type: application/octet-stream\n"
            'Content-Disposition: attachment; filename="filename.txt"\n'
            "Content-Encoding: gzip\n"
            "\n"
            "gAAAAABjLCBfkrBO5yJLi1dybS3v_egUxC63Qkh7TkuJL64uasQ_H0APGTq5oJT94JVPx3\n"
            "_mlLvVbQISEXyPAKKbRtDesX9AxKMDxrSYMtKKOcLsAYPigCQ=\n"
            "===== END BLOCK =====\n"
        )
        self.data_object_file_no_zip = DataObject(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename="filename.txt",
            binary_data="dataobject: file".encode("utf-8"),
        )
        self.data_object_file_no_zip_encrypted = (
            "gAAAAABjLCkL0G6QXaftdznNXf_qPmg4L0HZkqryb9mikihzWKfCLhOJYZwc9W7wch6D3a"
            "UoDk8vxQl_9zWIpvipdzYT9u1Z5WeIZilOT_W5Bo0LNlr2DBE="
        ).encode("ASCII")
        self.data_object_file_no_zip_block = (
            "===== START BLOCK =====\n"
            "Content-Type: application/octet-stream\n"
            'Content-Disposition: attachment; filename="filename.txt"\n'
            "\n"
            "gAAAAABjLCkL0G6QXaftdznNXf_qPmg4L0HZkqryb9mikihzWKfCLhOJYZwc9W7wch6D3a\n"
            "UoDk8vxQl_9zWIpvipdzYT9u1Z5WeIZilOT_W5Bo0LNlr2DBE=\n"
            "===== END BLOCK =====\n"
        )

    @mk.patch("crippy_app.secrets", spec_set=True)
    def test001_generate_salt_returns_at_least_16_bytes(self, mk_secrets):
        BlockCrypter.generate_salt()
        mk_secrets.token_bytes.assert_called()
        n_bytes = mk_secrets.token_bytes.call_args[0][0]
        self.assertGreaterEqual(n_bytes, 16)

    @mk.patch("crippy_app.PBKDF2HMAC", spec_set=True)
    def test002_derive_key_from_password(self, mk_pbkdf2hmac):
        mk_pbkdf2hmac.return_value.derive.return_value = self.DERIVED_KEY_BIN
        derived_key = BlockCrypter.derive_key_from_password(self.PASSWORD, self.SALT)
        self.assertEqual(derived_key, self.DERIVED_KEY)

    def test003_init(self):
        BlockCrypter(self.DERIVED_KEY)
        self.assertEqual(self.mk_fernet_init.mock_calls[0], mk.call(self.DERIVED_KEY))

    def test004_encrypt_to_block_none_as_dataobject(self):
        bc = BlockCrypter(self.DERIVED_KEY)
        with self.assertRaises(InvalidDataException) as exc:
            bc.encrypt_to_block(None)
        self.assertTrue("DataObject" in exc.exception.args[0])

    def test005_encrypt_to_block_none_as_binary_data(self):
        self.data_object_str.binary_data = None
        bc = BlockCrypter(self.DERIVED_KEY)
        with self.assertRaises(InvalidDataException) as exc:
            bc.encrypt_to_block(self.data_object_str)
        self.assertTrue("binary_data" in exc.exception.args[0])

    def test006_encrypt_to_block_none_as_content_type(self):
        self.data_object_str.content_type = None
        bc = BlockCrypter(self.DERIVED_KEY)
        with self.assertRaises(InvalidDataException) as exc:
            bc.encrypt_to_block(self.data_object_str)
        self.assertTrue("content_type" in exc.exception.args[0])

    def test007_encrypt_to_block_unsupported_content_type(self):
        self.data_object_str.content_type = "image/png"
        bc = BlockCrypter(self.DERIVED_KEY)
        with self.assertRaises(InvalidDataException) as exc:
            bc.encrypt_to_block(self.data_object_str)
        self.assertTrue("not supported" in exc.exception.args[0])

    def test008_encrypt_to_block_binary_data_is_encrypted(self):
        bc = BlockCrypter(self.DERIVED_KEY)
        bc.encrypt_to_block(self.data_object_str)
        self.assertEqual(self.mk_fernet_encrypt.mock_calls[0], mk.call(self.data_object_str.binary_data))

    def test009_encrypt_to_block_text_plain(self):
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_encrypt.return_value = self.data_object_str_encrypted
        block = bc.encrypt_to_block(self.data_object_str)
        self.assertEqual(block, self.data_object_str_block)

    def test010_encrypt_to_block_text_plain_no_charset(self):
        self.data_object_str.charset = None
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_encrypt.return_value = self.data_object_str_encrypted
        block = bc.encrypt_to_block(self.data_object_str)
        self.assertTrue("charset=" not in block)

    def test011_encrypt_to_block_application_octet_stream(self):
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_encrypt.return_value = self.data_object_file_encrypted
        block = bc.encrypt_to_block(self.data_object_file)
        self.assertEqual(block, self.data_object_file_block)

    def test012_encrypt_to_block_application_octet_stream_no_filename(self):
        self.data_object_file.filename = None
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_encrypt.return_value = self.data_object_file_encrypted
        block = bc.encrypt_to_block(self.data_object_file)
        self.assertTrue("filename=" not in block)

    def test013_encrypt_to_block_text_plain_width_0(self):
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_encrypt.return_value = self.data_object_str_encrypted
        block = bc.encrypt_to_block(self.data_object_str, width=0)
        expected_block_length = len(self.data_object_str_block.split("\n")) - 1
        self.assertEqual(len(block.split("\n")), expected_block_length)

    def test014_encrypt_to_block_text_plain_width_40_via_default(self):
        width = 40
        bc = BlockCrypter(self.DERIVED_KEY, width=width)
        self.mk_fernet_encrypt.return_value = self.data_object_str_encrypted
        block = bc.encrypt_to_block(self.data_object_str)
        max_line_length = max(len(line) for line in block.splitlines())
        self.assertEqual(max_line_length, width)

    def test015_encrypt_to_block_text_plain_width_40_via_argument(self):
        width = 40
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_encrypt.return_value = self.data_object_str_encrypted
        block = bc.encrypt_to_block(self.data_object_str, width=width)
        max_line_length = max(len(line) for line in block.splitlines())
        self.assertEqual(max_line_length, width)

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test016_decrypt_from_block_start_block_not_found(self, mk_create):
        bc = BlockCrypter(self.DERIVED_KEY)
        block = self.data_object_str_block.replace(bc._start_block, "")
        with self.assertRaises(InvalidBlockException) as exc:
            bc.decrypt_from_block(block)
        self.assertTrue("block markers" in exc.exception.args[0])

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test017_decrypt_from_block_end_block_not_found(self, mk_create):
        bc = BlockCrypter(self.DERIVED_KEY)
        block = self.data_object_str_block.replace(bc._end_block, "")
        with self.assertRaises(InvalidBlockException) as exc:
            bc.decrypt_from_block(block)
        self.assertTrue("block markers" in exc.exception.args[0])

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test018_decrypt_from_block_content_type_not_found(self, mk_create):
        content_type_marker = "Content-Type:"
        bc = BlockCrypter(self.DERIVED_KEY)
        block = self.data_object_str_block.replace(content_type_marker, "Missing:")
        with self.assertRaises(InvalidBlockException) as exc:
            bc.decrypt_from_block(block)
        self.assertTrue(content_type_marker in exc.exception.args[0])

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test019_decrypt_from_block_content_disposition_not_found(self, mk_create):
        content_disposition_marker = "Content-Disposition:"
        bc = BlockCrypter(self.DERIVED_KEY)
        block = self.data_object_str_block.replace(content_disposition_marker, "Missing:")
        with self.assertRaises(InvalidBlockException) as exc:
            bc.decrypt_from_block(block)
        self.assertTrue(content_disposition_marker in exc.exception.args[0])

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test020_decrypt_from_block_text_plain(self, mk_create):
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_decrypt.return_value = self.data_object_str.binary_data
        bc.decrypt_from_block(self.data_object_str_block)
        expected_call = mk.call("text/plain; charset=utf-8", "inline", None, self.data_object_str.binary_data)
        self.assertEqual(mk_create.mock_calls[0], expected_call)

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test021_decrypt_from_block_text_plain_no_charset(self, mk_create):
        bc = BlockCrypter(self.DERIVED_KEY)
        block = self.data_object_str_block.replace("; charset=utf-8", "")
        self.mk_fernet_decrypt.return_value = self.data_object_str.binary_data
        bc.decrypt_from_block(block)
        expected_call = mk.call("text/plain", "inline", None, self.data_object_str.binary_data)
        self.assertEqual(mk_create.mock_calls[0], expected_call)

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test022_decrypt_from_block_application_octet_stream(self, mk_create):
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_decrypt.return_value = self.data_object_file.binary_data
        bc.decrypt_from_block(self.data_object_file_block)
        expected_call = mk.call(
            "application/octet-stream", 'attachment; filename="filename.txt"', "gzip", self.data_object_file.binary_data
        )
        self.assertEqual(mk_create.mock_calls[0], expected_call)

    @mk.patch("crippy_app.BlockCrypter._create_dataobject", spec_set=True)
    def test023_decrypt_from_block_application_octet_stream_no_zip(self, mk_create):
        bc = BlockCrypter(self.DERIVED_KEY)
        self.mk_fernet_decrypt.return_value = self.data_object_file_no_zip_encrypted
        bc.decrypt_from_block(self.data_object_file_no_zip_block)
        expected_call = mk.call(
            "application/octet-stream",
            'attachment; filename="filename.txt"',
            None,
            self.data_object_file_no_zip_encrypted,
        )
        self.assertEqual(mk_create.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test024_create_dataobject_invalid_content_type(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("image/gif", 'attachment; filename="image.gif"', None, b"<gif_data>")
        with self.assertRaises(InvalidContentException) as exc:
            bc._create_dataobject(*args)
        self.assertTrue("content_type" in exc.exception.args[0])
        self.assertTrue(args[0] in exc.exception.args[0])

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test025_create_dataobject_invalid_content_encoding(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("application/octet-stream", 'attachment; filename="image.zip"', "deflate", b"<gif_data>")
        with self.assertRaises(InvalidContentException) as exc:
            bc._create_dataobject(*args)
        self.assertTrue("content_encoding" in exc.exception.args[0])
        self.assertTrue(args[2] in exc.exception.args[0])

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test026_create_dataobject_text_plain_with_charset_no_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("text/plain; charset=utf-8", "inline", None, b"<data placeholder>")
        expected_call = mk.call(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=False,
            filename=None,
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test027_create_dataobject_text_plain_no_charset_no_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("text/plain", "inline", None, b"<data placeholder>")
        expected_call = mk.call(
            content_type="text/plain",
            charset=None,
            is_zipped=False,
            filename=None,
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test028_create_dataobject_text_plain_with_charset_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("text/plain; charset=utf-8", "inline", "gzip", b"<data placeholder>")
        expected_call = mk.call(
            content_type="text/plain",
            charset="utf-8",
            is_zipped=True,
            filename=None,
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test029_create_dataobject_text_plain_no_charset_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("text/plain", "inline", "gzip", b"<data placeholder>")
        expected_call = mk.call(
            content_type="text/plain",
            charset=None,
            is_zipped=True,
            filename=None,
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test030_create_dataobject_application_octet_stream_with_filename_no_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("application/octet-stream", 'attachment; filename="text.txt"', None, b"<data placeholder>")
        expected_call = mk.call(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename="text.txt",
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test031_create_dataobject_application_octet_stream_no_filename_no_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("application/octet-stream", "attachment", None, b"<data placeholder>")
        expected_call = mk.call(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=False,
            filename=None,
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test032_create_dataobject_application_octet_stream_with_filename_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("application/octet-stream", 'attachment; filename="text.txt"', "gzip", b"<data placeholder>")
        expected_call = mk.call(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=True,
            filename="text.txt",
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test033_create_dataobject_application_octet_stream_no_filename_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = ("application/octet-stream", "attachment", "gzip", b"<data placeholder>")
        expected_call = mk.call(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=True,
            filename=None,
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)

    @mk.patch("crippy_app.DataObject", spec_set=True)
    def test034_create_dataobject_application_octet_stream_with_spaces_in_filename_zip(self, mk_data_obj):
        bc = BlockCrypter(self.DERIVED_KEY)
        args = (
            "application/octet-stream",
            'attachment; filename="this name contains spaces.txt"',
            "gzip",
            b"<data placeholder>",
        )
        expected_call = mk.call(
            content_type="application/octet-stream",
            charset=None,
            is_zipped=True,
            filename="this name contains spaces.txt",
            binary_data=b"<data placeholder>",
        )
        bc._create_dataobject(*args)
        self.assertEqual(mk_data_obj.mock_calls[0], expected_call)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
