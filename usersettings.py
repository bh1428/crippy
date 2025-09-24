#!/usr/bin/env python3
"""Manage user settings using a (user and platform specific) file."""

import json
import pathlib
from typing import Any

from platformdirs import PlatformDirs


class UserSettings:
    """Manage user settings using a (user and platform specific) file.

    This class will save / load settings to / from a user (and platform)
    specific system file. The file is supposed to be a JSON dump of a Python
    dictionary. Only the standard JSON conversions are supported, see:
    https://docs.python.org/3/library/json.html?highlight=json#py-to-json-table

    The default filename (can be overruled) is: settings.json
    """

    DEFAULT_FILENAME = "settings.json"

    def __init__(
        self,
        app_name: str,
        app_author: None | str = None,
        filename: None | str | pathlib.Path = None,
        roaming: bool = False,
    ) -> None:
        r"""Create a new UserSettings instance.

        The path for the settings file is constructed from three components:
            <platform_specific_base>/<app_author>/<app_name>/<filename>
        For example (on 'modern' Windows):
            `C:\Users\username\AppData\Local\app_author\app_name\settings.json`
        Or on Linux:
            `/home/username/.config/app_name/settings.json`

        Notes:
          * On Windows: by setting `roaming` to `True` you can choose to
            use the local application data (default) or the roaming
            application data directory.
          * The `app_author` name is only used on Windows. If (on Windows) no
            `app_author` is provided the `app_name` will be used twice, e.g.:
                `...\app_name\app_name\settings.json`.

        Args:
            app_name (str): application name
            app_author (None | str, optional): author / publisher (only
                relevant on Windows)
            filename (None | str | pathlib.Path, optional): filename for the
                settings file, default: `UserSettings.DEFAULT_FILENAME`.
            roaming (bool, optional): only relevant on Windows: roaming or
                local directory, defaults to local (`roaming=False`).
        """
        self.platformdirs = PlatformDirs(appname=app_name, appauthor=app_author, roaming=roaming)
        if not self.platformdirs.user_config_path.exists():
            self.platformdirs.user_config_path.mkdir(parents=True)
        if filename is None:
            self.user_settings_file = self.platformdirs.user_config_path / self.DEFAULT_FILENAME
        else:
            self.user_settings_file = self.platformdirs.user_config_path / pathlib.Path(filename).name

    @property
    def settings(self) -> dict:
        """Get all settings at once."""
        if self.user_settings_file.exists():
            return json.loads(self.user_settings_file.read_text(encoding="ansi"))
        return {}

    @settings.setter
    def settings(self, value: dict) -> None:
        """Set all settings at once.

        Args:
            value (dict): settings dictionary to be stored

        Raises:
            TypeError: is raised when the `value` is not a dictionary
        """
        if isinstance(value, dict):
            self.user_settings_file.write_text(json.dumps(value), encoding="ansi")
        else:
            raise TypeError(f"operand type must be a 'dict', got: '{type(value).__name__}'")

    def get(self, name: str, default: Any = None) -> Any:
        """Get a setting or a default when missing.

        Args:
            name (name): setting to be retrieved
            default (Any, optional): default value when `name` is not found

        Returns:
            Any: setting or default value (`None` when not provided)
        """
        try:
            return self[name]
        except KeyError:
            return default

    def __getitem__(self, name: str) -> Any:
        """Get a single setting.

        Args:
            name (str): setting name

        Returns:
            Any: setting value
        """
        return self.settings[name]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a single setting.

        Args:
            key (str): name of the setting
            value (Any): value for the settings
        """
        current_settings = self.settings
        current_settings[key] = value
        self.settings = current_settings
