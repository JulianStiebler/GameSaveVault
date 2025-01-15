"""
GameSaveVault - A tool for managing and backing up game save files.

Copyright (C) 2025 Julian Stiebler (stblr)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

GitHub Repository: https://github.com/JulianStiebler/GameSaveVault
GitHub License: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
GitHub License File: https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

Last Edited: 16.01.2025
"""

from enum import Enum, auto
from pathlib import Path
import os

class DataFolder(Enum):
    """Application data folders"""
    DATAROOT = "data"
    SAVEGAMES = f"{DATAROOT}/savegames"

    def __str__(self):
        return str(self.value)

class DataFile(Enum):
    """Application data files"""
    DATAROOT = Path(DataFolder.DATAROOT.value)
    APPID = Path(DataFolder.DATAROOT.value) / "appid.json"
    INSTALLED_GAMES = Path(DataFolder.DATAROOT.value) / "installedGames.json"
    KNOWN_PATHS = Path(DataFolder.DATAROOT.value) / "knownGamePaths.json"
    CUSTOM_GAMES = Path(DataFolder.DATAROOT.value) / "customGames.json"

    def __str__(self):
        return str(self.value)

    @property
    def exists(self) -> bool:
        return Path(self.value).exists()

class Platform(Enum):
    """Gaming platforms supported by the application"""
    STEAM = "Steam"
    EPIC = "Epic" 
    GENERAL = "General"
    CUSTOM = "Custom"
    
class PathType(Enum):
    """Types of paths in the application"""
    SAVE = "save"
    INSTALL = "install"

class BackupType(Enum):
    """Types of game save backups"""
    TIMESTAMPED = auto()
    NAMED = auto()

class RegistryKeys(Enum):
    """Registry keys used for platform detection"""
    STEAM = r"SOFTWARE\Valve\Steam"
    EPIC = r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher"

class SystemPaths(Enum):
    """System environment paths"""
    GAME_INSTALL = "%gameinstall%"  # First priority
    LOCAL_APPDATA = "%LOCALAPPDATA%"
    APPDATA = "%APPDATA%"
    PROGRAM_FILES = "%PROGRAMFILES%"
    PROGRAM_FILES_X86 = "%PROGRAMFILES(X86)%"
    USER_PROFILE = "%USERPROFILE%"
    DOCUMENTS = "%USERPROFILE%\\Documents"
    
    def resolve(self) -> Path:
        return Path(os.path.expandvars(self.value))
    
class PublicSources(Enum):
    """API endpoints used by the application"""
    STEAM_APPLIST = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    
class AppStates(Enum):
    DEBUG = "DEBUG"
    RELEASE = "RELEASE"
    
class AppConfig(Enum):
    """Application configuration constants"""
    VERSION = "Version 1-beta"
    WINDOW_SIZE_X = 1000
    WINDOW_SIZE_Y = 800
    WINDOW_GEOMETRY = f"{WINDOW_SIZE_X}x{WINDOW_SIZE_Y}"
    WINDOW_THEME = "darkly"
    WINDOW_TITLE = "Game Save Vault"
    STATE = AppStates.DEBUG
    
class AppConfigGithub(Enum):
    GITHUB_URL = "https://github.com/"
    GITHUB_ORIGIN = "JulianStiebler"
    GITHUB_PROJECT = "GameSaveVault"
    GITHUB_ASSIGNEES = f"{GITHUB_ORIGIN}"
    GITHUB_URL_ORIGIN = f"{GITHUB_URL}/{GITHUB_ORIGIN}/{GITHUB_PROJECT}/tree/main"
    GITHUB_URL_FEATUREREQUEST = f"{GITHUB_URL}/{GITHUB_ORIGIN}/{GITHUB_PROJECT}/issues/new?assignees={GITHUB_ASSIGNEES}&labels=feature&projects=&template=feature_request.md&title=Feature+request"
    GITHUB_URL_BUGREPORT = f"{GITHUB_URL}/{GITHUB_ORIGIN}/{GITHUB_PROJECT}/issues/new?assignees={GITHUB_ASSIGNEES}&labels=bug&projects=&template=bug_report.md&title=Bug+report"
