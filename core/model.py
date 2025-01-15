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

from dataclasses import dataclass, field, asdict
from typing import Dict, Optional, List, ClassVar
from datetime import datetime
from pathlib import Path
import os
import json

from .enums import Platform, PathType, DataFile, BackupType, SystemPaths

@dataclass
class GameMetadata:
    name: str
    appid: Optional[str] = None
    platform: Platform = None
    install_dir: Optional[str] = None
    header_image: Optional[str] = None
    manual_url: Optional[str] = None
    guide_url: Optional[str] = None
    wiki_url: Optional[str] = None
    version: Optional[str] = None
    last_updated: datetime = field(default_factory=datetime.now)

@dataclass
class PathInfo:
    """Base class for path management"""
    _system_paths: ClassVar[Dict[str, str]] = {
        SystemPaths.LOCAL_APPDATA.value: os.environ.get('LOCALAPPDATA', ''),
        SystemPaths.APPDATA.value: os.environ.get('APPDATA', ''),
        SystemPaths.PROGRAM_FILES.value: os.environ.get('PROGRAMFILES', ''),
        SystemPaths.PROGRAM_FILES_X86.value: os.environ.get('PROGRAMFILES(X86)', ''),
        SystemPaths.USER_PROFILE.value: os.environ.get('USERPROFILE', '')
    }

    @classmethod
    def get_game_install_path(cls, game_name: str) -> Optional[str]:
        try:
            with open(DataFile.INSTALLED_GAMES, 'r') as f:
                installed_games = json.load(f)
                
            if game_name in installed_games:
                return installed_games[game_name].get('pathInstall')
        except Exception as e:
            print(f"Error reading game install path: {e}")
        return None

    @classmethod
    def to_absolute(cls, path: str, game_name: Optional[str] = None) -> str:
        """Convert path to absolute with game install path resolution"""
        if SystemPaths.GAME_INSTALL.value in path and game_name:
            game_install = cls.get_game_install_path(game_name)
            if game_install:
                path = path.replace(SystemPaths.GAME_INSTALL.value, game_install)
        return os.path.normpath(os.path.expandvars(path))

    @classmethod
    def to_relative(cls, path: str) -> str:
        """Convert absolute path to relative"""
        if cls.is_relative(path):
            return path
            
        normalized = os.path.normpath(path).lower()
        for env_var, sys_path in sorted(
            cls._system_paths.items(),
            key=lambda x: len(x[1].split(os.sep)),
            reverse=True
        ):
            if normalized.startswith(sys_path.lower()):
                return path.replace(sys_path, env_var)
        return path

    @classmethod
    def is_relative(cls, path: str) -> bool:
        """Check if path contains environment variables"""
        return any(var.lower() in path.lower() for var in cls._system_paths)

@dataclass
class GamePath(PathInfo):
    path: str
    type: PathType
    _absolute_path: Optional[str] = field(default=None, init=False)
    
    def __post_init__(self):
        self._absolute_path = None
    
    @property
    def absolute(self) -> str:
        """Get absolute path"""
        if not self._absolute_path:
            self._absolute_path = self.to_absolute(self.path)
        return self._absolute_path
    
    @property
    def relative(self) -> str:
        """Get relative path"""
        return self.to_relative(self.path)
    
    @property
    def exists(self) -> bool:
        """Check if path exists"""
        return Path(self.absolute).exists()

    def update(self, new_path: str):
        """Update path and reset absolute cache"""
        self.path = new_path
        self._absolute_path = None
        
@dataclass
class Game:
    metadata: GameMetadata
    paths: Dict[PathType, GamePath] = field(default_factory=dict)
    
    @property
    def name(self) -> str:
        return self.metadata.name
    
    def to_dict(self) -> dict:
        return {
            "metadata": asdict(self.metadata),
            "paths": {k.name: v.path for k, v in self.paths.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Game':
        metadata = GameMetadata(**data["metadata"])
        paths = {
            PathType[k]: GamePath(path=v, type=PathType[k])
            for k, v in data["paths"].items()
        }
        return cls(metadata=metadata, paths=paths)
    
    def get_path(self, path_type: PathType, relative: bool = False) -> Optional[str]:
        """Get path of specified type"""
        if path_type not in self.paths:
            return None
        return self.paths[path_type].relative if relative else self.paths[path_type].absolute
    
    def set_path(self, path_type: PathType, path: str):
        """Set or update path"""
        if path_type in self.paths:
            self.paths[path_type].update(path)
        else:
            self.paths[path_type] = GamePath(path=path, type=path_type)

@dataclass
class GameLibrary:
    games: Dict[str, Game] = field(default_factory=dict)
    
    def add_game(self, game: Game):
        self.games[game.name] = game
    
    def get_by_platform(self, platform: Platform) -> List[Game]:
        return [game for game in self.games.values() 
                if game.metadata.platform == platform]

@dataclass
class Backup:
    game_name: str
    path: Path
    type: BackupType
    created_at: datetime = field(default_factory=datetime.now)
    description: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "game_name": self.game_name,
            "path": str(self.path),
            "type": self.type.name,
            "created_at": self.created_at.isoformat(),
            "description": self.description
        }

        
@dataclass
class GameResource:
    """Resource links for a game (manual, guides etc)"""
    url: str
    type: str
    title: Optional[str] = None
    language: str = "en"
    
@dataclass 
class AppState:
    """Application state tracking"""
    selected_game: Optional[str] = None
    current_platform: Platform = None
    has_unsaved_changes: bool = False
    last_backup_path: Optional[Path] = None