#!/usr/bin/env python3
"""Encrypt / decrypt text and files to and from BASE64 encoded blocks."""

import pathlib
import sys

from PySide6 import QtCore, QtWidgets

import crippy_app
import crippy_ui
from usersettings import UserSettings

__version__ = "1.0.0"
__copyright__ = "<br>".join(
    [
        "Copyright (C) 2021-2025  Ben Hattem",
        "",
        "This program comes with ABSOLUTELY NO WARRANTY.",
        "This is free software, and you are welcome to redistribute it under certain conditions.",
    ]
)


def msg_with_correct_plural(template: str, number: int) -> str:
    """Generate a grammatically correct message.

    The template is supposed to have two placeholders: the first is for the
    number and the second is for an optional 's'. For example, given this
    template: "Counted {} rabbit{}", the following results can be created:
        number=1: "Counted 1 rabbit"
        number=2: "Counted 2 rabbits"

    Args:
        template (str): message template
        number (int): number to be inserted in the template

    Returns:
        str: formatted message
    """
    s_or_no_s = "" if number == 1 else "s"
    str_number = f"{number:,}".replace(",", ".")
    return template.format(str_number, s_or_no_s)


class MainWindow(QtWidgets.QMainWindow, crippy_ui.Ui_MainWindow):
    """Main windows for the crippy application."""

    LAST_LOAD_PATH = "LAST_LOAD_PATH"
    LAST_SAVE_PATH = "LAST_SAVE_PATH"

    def __init__(self) -> None:
        super().__init__()
        self.settings = UserSettings("crippy", "nl.benhattem")
        self.setupUi(self)

    def reset_gui(self) -> None:
        """Reset the entire GUI state."""
        self.le_password.clear()
        self.cb_show_password.setChecked(False)
        self.le_filename.clear()
        self.te_input.clear()
        self.te_output.clear()
        self.status_bar.clearMessage()

    @QtCore.Slot()
    def on_file_new_triggered(self) -> None:
        """Menu: File -> New"""
        self.reset_gui()

    @QtCore.Slot()
    def on_file_exit_triggered(self) -> None:
        """Menu: File -> Exit"""
        self.close()

    @QtCore.Slot()
    def on_help_about_triggered(self) -> None:
        """Menu: Help -> About"""
        about_text = "<br>".join(
            [
                f"<b>crippy</b> V{__version__}",
                "",
                __copyright__,
                "",
                "Encrypt / decrypt text and files to and from BASE64 encoded blocks.",
            ]
        )
        QtWidgets.QMessageBox.about(self, "About", about_text)

    @QtCore.Slot()
    def on_cb_show_password_stateChanged(self) -> None:  # pylint: disable=invalid-name
        """Action when the 'Show password' option is changed."""
        if self.cb_show_password.isChecked():
            self.le_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.le_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.status_bar.clearMessage()

    @QtCore.Slot()
    def on_te_input_textChanged(self) -> None:  # pylint: disable=invalid-name
        """Action when the 'Input' changes'."""
        self.te_output.clear()
        self.status_bar.clearMessage()

    def select_file_dialog(self, save: bool = False, overrule_filename: None | str = None) -> str:
        """Select a file using a standard dialog.

        The content of the filename input line is used as a filename proposal
        unless it is overruled via the `overrule_filename` argument.

        Args:
            save (bool, optional): by default an 'Open' dialog is used, by
                setting this to True a 'Save' dialog is used.
            overrule_filename (str, optional): option to overrule the filename
                from the filename input line

        Returns:
            str: selected file (full path)
        """
        # last path ois persisted in settings
        setting = self.LAST_LOAD_PATH
        if save:
            setting = self.LAST_SAVE_PATH
        # use the filename field as a proposal
        start_path = pathlib.Path(self.settings.get(setting, pathlib.Path.cwd()))
        if overrule_filename is None:
            given_filename = self.le_filename.text()
        else:
            given_filename = overrule_filename
        if given_filename:
            # strip path when present
            start_path = start_path / pathlib.Path(given_filename).name
        str_start_path = str(start_path)

        # present dialog
        if save:
            (filename, _) = QtWidgets.QFileDialog.getSaveFileName(
                self, caption="Save File", dir=str_start_path, filter="All Files (*.*)"
            )
        else:
            (filename, _) = QtWidgets.QFileDialog.getOpenFileName(
                self, caption="Open File", dir=str_start_path, filter="All Files (*.*)"
            )

        # update filename field when needed and return result
        if (overrule_filename is None) and filename:
            path_filename = pathlib.Path(filename)
            self.settings[setting] = str(path_filename.parent)
            self.le_filename.setText(path_filename.name)
        return filename

    def encrypt(self, data: crippy_app.DataObject) -> str:
        """Encrypt a DataObject to a text block.

        Args:
            data (crippy_app.DataObject): DataObject to be encrypted

        Returns:
            str: text block with encrypted result (including headers)
        """
        key = crippy_app.BlockCrypter.derive_key_from_password(self.le_password.text(), salt=crippy_app.SALT)
        block_crypter = crippy_app.BlockCrypter(key)
        encrypted_data = block_crypter.encrypt_to_block(data)
        len_data = 0 if data.binary_data is None else len(data.binary_data)
        self.status_bar.showMessage(msg_with_correct_plural("Encrypted {} byte{}...", len_data))
        return encrypted_data

    @QtCore.Slot()
    def on_encrypt_input_to_output_triggered(self) -> None:
        """Menu: Encrypt -> 'Input -> Output'."""
        encrypted_block = self.encrypt(crippy_app.DataObject.from_str(self.te_input.toPlainText()))
        self.te_output.setPlainText(encrypted_block)

    def _encrypt_file(self, filename: str | pathlib.Path) -> None:
        """Encrypt a file to the output.

        Args:
            filename (str | pathlib.Path): name of the file to encrypt
        """
        if filename:
            self.te_input.clear()
            encrypted_block = self.encrypt(crippy_app.DataObject.from_file(filename))
            self.te_output.setPlainText(encrypted_block)

    @QtCore.Slot()
    def on_encrypt_file_to_output_triggered(self) -> None:
        """Menu: Encrypt -> 'File -> Output'."""
        filename = self.select_file_dialog()
        self._encrypt_file(filename)

    def decrypt(self) -> crippy_app.DataObject:
        """Decrypt a text block to a DataObject.

        The input for the decrypt operation is always the 'Input' text editor.

        Returns:
            crippy_app.DataObject: decrypted result
        """
        # make sure we have input
        input_text = self.te_input.toPlainText()
        if not input_text:
            QtWidgets.QMessageBox.critical(
                self,
                "No input",
                "There is no input.\n\nPlease provide an input block...\n",
                QtWidgets.QMessageBox.StandardButton.Ok,
                QtWidgets.QMessageBox.StandardButton.NoButton,
            )
            return crippy_app.DataObject.from_str("")

        # decrypt the input text block
        key = crippy_app.BlockCrypter.derive_key_from_password(self.le_password.text(), salt=crippy_app.SALT)
        block_crypter = crippy_app.BlockCrypter(key)
        try:
            decrypted_data = block_crypter.decrypt_from_block(input_text)
        except Exception:  # pylint: disable=broad-except
            # catch all exceptions (probably: wrong password or corrupt input)
            QtWidgets.QMessageBox.critical(
                self,
                "Decryption error",
                "Could not decrypt input.\n\nPlease check your password...\n",
                QtWidgets.QMessageBox.StandardButton.Ok,
                QtWidgets.QMessageBox.StandardButton.NoButton,
            )
            return crippy_app.DataObject.from_str("")

        # keep an (optional) filename and report on result
        if decrypted_data.filename is not None:
            self.le_filename.setText(str(pathlib.Path(decrypted_data.filename).name))  # strip path
        len_data = 0 if decrypted_data.binary_data is None else len(decrypted_data.binary_data)
        self.status_bar.showMessage(msg_with_correct_plural("Decrypted {} byte{}", len_data))
        return decrypted_data

    @QtCore.Slot()
    def on_decrypt_input_to_output_triggered(self) -> None:
        """Menu: Decrypt -> 'Input -> Output'."""
        decrypted_data = self.decrypt()
        if decrypted_data.binary_data:
            if (output_text := decrypted_data.as_str()) is None:
                output_text = ""
            self.te_output.setPlainText(output_text)
        self.status_bar.showMessage(f"{self.status_bar.currentMessage()}...")

    @QtCore.Slot()
    def on_decrypt_input_to_file_triggered(self) -> None:
        """Menu: Decrypt -> 'Input -> File'."""
        decrypted_data = self.decrypt()
        if decrypted_data.binary_data:
            filename = self.select_file_dialog(save=True)
            if filename:
                self.te_output.clear()
                decrypted_data.to_file(filename)
                self.status_bar.showMessage(f"{self.status_bar.currentMessage()}, saved to '{filename}'...")
            else:
                self.status_bar.showMessage(f"{self.status_bar.currentMessage()}, NOT saved (cancelled)...")

    @QtCore.Slot()
    def on_pb_encrypt_from_file_clicked(self) -> None:
        """Button: [Encrypt from File]."""
        self.on_encrypt_file_to_output_triggered()

    @QtCore.Slot()
    def on_pb_decrypt_to_file_clicked(self) -> None:
        """Button: [Decrypt to File]."""
        self.on_decrypt_input_to_file_triggered()

    @QtCore.Slot()
    def on_pb_encrypt_clicked(self) -> None:
        """Button: [Encrypt]."""
        self.on_encrypt_input_to_output_triggered()

    @QtCore.Slot()
    def on_pb_decrypt_clicked(self) -> None:
        """Button: [Decrypt]."""
        self.on_decrypt_input_to_output_triggered()

    @QtCore.Slot(pathlib.Path)  # type: ignore
    def on_te_input_file_dropped(self, filename: pathlib.Path) -> None:
        """File dropped in input"""
        self.settings[self.LAST_LOAD_PATH] = str(filename.parent)
        self._encrypt_file(filename)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
