#!/usr/bin/env python3
"""QPlainTextEdit with drag and drop support for files."""

import pathlib
from typing import Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPlainTextEdit


class MyPlainTextEdit(QPlainTextEdit):
    """QPlainTextEdit with drag and drop support for files.

    This widget will emit a signal `file_dropped` (with the filename) when a
    file is dropped.
    """

    file_dropped = Signal(pathlib.Path)

    def dragEnterEvent(self, event: Any) -> None:
        """Accept drag events for URLs (i.e. filenames)"""
        if event.mimeData().hasUrls():
            event.accept()
        super().dragEnterEvent(event)

    def dropEvent(self, event: Any) -> None:
        """Handle a drop event."""
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            url = mime_data.urls()[0]
            filename = pathlib.Path(url.toLocalFile())
            self.file_dropped.emit(filename)
        else:
            super().dropEvent(event)
