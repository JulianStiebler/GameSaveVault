# core/enums.py
from enum import Enum, auto
from pathlib import Path
from pydantic import AnyUrl
import os
from typing import Optional, Union, List, Dict

class DataFolder(Enum):
    """Application data folders"""
    DATAROOT = "data"
    SAVEGAMES = f"{DATAROOT}/savegames"
    PATHS = f"{DATAROOT}/paths"

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
    BACKUP = "backup"
    CONFIG = "config"

class BackupType(Enum):
    """Types of game save backups"""
    TIMESTAMPED = auto()
    NAMED = auto()

class FileType(Enum):
    """Types of special files in the application"""
    SAVE = auto()
    INSTALL = auto()
    BACKUP = auto()

class RegistryKeys(Enum):
    """Registry keys used for platform detection"""
    STEAM = r"SOFTWARE\Valve\Steam"
    EPIC = r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher"

class SystemPaths(Enum):
    """System environment paths"""
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
    
class GameResource(Enum):
    """Types of game resources"""
    MANUAL = "manual"
    GUIDE = "guide" 
    WIKI = "wiki"
    HEADER = "header_image"
    
class AppConfig(Enum):
    """Application configuration constants"""
    VERSION = "Version 0.9.9-alpha"
    WINDOW_SIZE_X = 1000
    WINDOW_SIZE_Y = 800
    WINDOW_GEOMETRY = f"{WINDOW_SIZE_X}x{WINDOW_SIZE_Y}"
    THEME = "darkly"
    TITLE = "Game Save Vault"
    
class AppConfigGithub(Enum):
    GITHUB_VERSION = "Version 1-beta"
    GITHUB_ORIGIN = "JulianStiebler"
    GITHUB_PROJECT = "GameSaveVault"
    GITHUB_ASSIGNEES = f"{GITHUB_ORIGIN}"
    GITHUB_URL = "https://github.com/"
    GITHUB_URL_ORIGIN = f"{GITHUB_URL}/{GITHUB_ORIGIN}/{GITHUB_PROJECT}/tree/main"
    GITHUB_URL_FEATUREREQUEST = f"{GITHUB_URL}/{GITHUB_ORIGIN}/{GITHUB_PROJECT}/issues/new?assignees={GITHUB_ASSIGNEES}&labels=feature&projects=&template=feature_request.md&title=Feature+request"
    GITHUB_URL_BUGREPORT = f"{GITHUB_URL}/{GITHUB_ORIGIN}/{GITHUB_PROJECT}/issues/new?assignees={GITHUB_ASSIGNEES}&labels=bug&projects=&template=bug_report.md&title=Bug+report"
