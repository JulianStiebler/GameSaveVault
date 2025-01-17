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

import json
from datetime import datetime
from pathlib import Path

from .model import PathInfo, GameLibrary, GameMetadata, Game, GamePath
from .enums import DataFile, DataFolder, PathType
from .util import Utility
from .detect import DetectSystem

class DataManager:
    def __init__(self):
        # Initialize paths
        self.DATA_STEAM_library = {}
        self.DATA_EPIC_library = {}
        self.DATA_GEN_library = {}
        self.DATA_JSONinstalledGames = {}
        self.DATA_JSONknownGamePaths = {}
        self.DATA_JSONcustomGames = {}
        
        self.PATH_steamLibrary = None
        self.PATH_epicLibrary = None
        
        # Create required directories
        Path(DataFolder.DATAROOT.value).mkdir(exist_ok=True)  # Use DataFolder instead of DataFile
        Path(DataFolder.SAVEGAMES.value).mkdir(exist_ok=True)

        self.detectSystem = DetectSystem(self)
        self.utility = Utility()

    def initApplication(self):
        self.DATA_JSONinstalledGames = self.loadJSON(DataFile.INSTALLED_GAMES.value, convertRelativePaths=True)
        self.DATA_JSONinstalledGamesNew = self.loadJSONNew(DataFile.INSTALLED_GAMES.value)
        
        self.DATA_JSONknownGamePaths = self.loadJSON(DataFile.KNOWN_PATHS.value)
        self.DATA_JSONknownGamePathsNew = self.loadJSONNew(DataFile.KNOWN_PATHS.value)
        
        self.DATA_JSONcustomGames = self.loadJSON(DataFile.CUSTOM_GAMES.value)

    @staticmethod
    def loadJSON(filePath, convertRelativePaths=False):
        """
        Load JSON data from a file.
        """
        try:
            # Convert Path object to string if needed
            file_path_str = str(filePath) if isinstance(filePath, Path) else filePath
            
            with open(file_path_str, 'r') as f:
                data = json.load(f)
                
                if convertRelativePaths and "installedGames" in file_path_str:
                    # Convert paths to absolute for in-memory use
                    for game_data in data.values():
                        if 'pathSave' in game_data:
                            game_data['pathSave'] = PathInfo.to_absolute(
                                game_data['pathSave'],
                                game_data.get('pathInstall')
                            )
                        if 'pathInstall' in game_data:
                            game_data['pathInstall'] = PathInfo.to_absolute(
                                game_data['pathInstall']
                            )
                
                return data
        except FileNotFoundError:
            print(f"File not found: {filePath}")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {filePath}: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error reading file {filePath}: {e}")
            return {}
        
    # Rework
    @staticmethod
    def loadJSONNew(filePath: Path) -> GameLibrary:
        """
        Load JSON data from a file and convert it into the appropriate models.

        :param filePath: Path to the JSON file.
        :return: An instance of GameLibrary or the raw data if conversion fails.
        """
        try:
            # Convert Path object to string if needed
            file_path_str = str(filePath) if isinstance(filePath, Path) else filePath

            with open(file_path_str, 'r') as f:
                raw_data = json.load(f)

            gameLibrary: GameLibrary = GameLibrary()

            for game_name, game_data in raw_data.items():
                # Extract metadata
                metadata = GameMetadata(
                    name=game_name,
                    appid=game_data.get("appid"),
                    platform=game_data.get("platform"),
                    install_dir=game_data.get("pathInstall"),
                    header_image=game_data.get("headerImage"),
                    manual_url=game_data.get("manualURL"),
                    guide_url=game_data.get("guideURL"),
                    wiki_url=game_data.get("wikiURL"),
                    version=game_data.get("version"),
                    last_updated=game_data.get("lastUpdated", datetime.now())
                )

                # Extract paths
                paths = {
                    PathType[path_key]: GamePath(path=path_value, type=PathType[path_key])
                    for path_key, path_value in game_data.get("paths", {}).items()
                }

                # Create Game object and add to library
                game = Game(metadata=metadata, paths=paths)
                gameLibrary.add_game(game)

            return gameLibrary
        
        except FileNotFoundError:
            print(f"File not found: {filePath}")
            return GameLibrary()  # Return an empty library if file not found
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {filePath}: {e}")
            return GameLibrary()  # Return an empty library if JSON invalid
        except Exception as e:
            print(f"Unexpected error reading file {filePath}: {e}")
            return GameLibrary()  # Return an empty library on any other error
        
    @staticmethod
    def saveJSON(filePath, data):
        """
        Save a dictionary or JSON-serializable object to a file.
        
        Args:
            file_path (str): Path to the JSON file to save.
            data (dict or list): Data to save to the JSON file.
        """
        try:
            with open(filePath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Successfully saved JSON data to {filePath}.")
        except Exception as e:
            print(f"Failed to save JSON data to {filePath}: {e}")
            
    @staticmethod
    def getTimestamp():
        """Get the current date and time as a formatted string."""
        return datetime.now().strftime("%d-%m-%Y-%H%M%S")
