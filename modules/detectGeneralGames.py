"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import os
import json
from pathlib import Path

from dataclasses import dataclass
from pathlib import Path
import json
import os
from typing import Dict, Optional

@dataclass
class GamePath:
    """Represents a single game's save path configuration"""
    name: str
    raw_path: str  # Original path from JSON with variables
    expanded_path: Optional[str] = None  # Path after variable expansion
    exists: bool = False
    platform: str = "General"

class KnownGamePaths:
    def __init__(self, data_manager):
        self.data = data_manager
        self.paths: Dict[str, GamePath] = {}
    
    def load_paths(self) -> None:
        """Load paths from knownGamePaths.json"""
        try:
            with open(self.data.PATH_knownGamePaths, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for game_name, path in data.get("Savepaths", {}).items():
                    self.paths[game_name] = GamePath(
                        name=game_name,
                        raw_path=path
                    )
        except FileNotFoundError:
            print(f"Known game paths file not found: {self.data.PATH_knownGamePaths}")
        except json.JSONDecodeError:
            print(f"Invalid JSON in: {self.data.PATH_knownGamePaths}")

    def expand_path(self, game_path: GamePath, installed_games: dict) -> None:
        """Expand variables in path"""
        path = game_path.raw_path
        
        if "%gameinstall%" in path and game_path.name in installed_games:
            install_path = installed_games[game_path.name].get('install_path')
            if install_path:
                path = path.replace("%gameinstall%", install_path)
        
        path = os.path.expandvars(path)
        game_path.expanded_path = os.path.normpath(path)
        game_path.exists = Path(game_path.expanded_path).exists()

class DetectGamesGeneral:
    def __init__(self, data):
        self.data = data
        
    def GetSaveFolders(self):
        def helper_expandPath(path: str, installedGames: dict, game: str) -> str:
            """Helper function to expand path and resolve '%gameinstall%'."""
            # Check if the path contains '%gameinstall%' and resolve it
            if "%gameinstall%" in path:
                # Ensure the game exists in installedGames
                if game in installedGames and 'install_path' in installedGames[game]:
                    # Replace '%gameinstall%' with the install_path
                    install_path = installedGames[game]['install_path']
                    path = path.replace("%gameinstall%", install_path)
                else:
                    print(f"Install path for '{game}' not found in installedGames.json.")
                    return None
            # Normalize and expand the path
            expandedPath = os.path.expandvars(path)
            return os.path.normpath(expandedPath)

        # Read the input JSON file containing save paths
        try:
            with open(self.data.PATH_knownGamePaths, 'r') as f:
                inputData = json.load(f)
        except FileNotFoundError:
            print(f"Input JSON file '{self.data.PATH_knownGamePaths}' not found.")
            return
        
        try:
            with open(self.data.PATH_installedGames, 'r') as f:
                installedGames = json.load(f)
        except FileNotFoundError:
            print(f"Installed games file '{self.data.PATH_installedGames}' not found.")
            return
        except Exception as e:
            print(f"Error reading '{self.data.PATH_installedGames}': {e}")
            return
        
        # Iterate through the game paths in the input JSON and check if they exist
        for game, path in inputData.get("Savepaths", {}).items():
            # Get the expanded save path
            expandedPath = helper_expandPath(path, installedGames, game)

            if expandedPath is None:
                continue

            # Debugging: print the expanded path to check if it's correct
            print(f"Checking save path for '{game}': {expandedPath}")

            # Ensure path ends with a backslash
            if not expandedPath.endswith(os.sep):
                expandedPath = expandedPath + os.sep

            # Check if the path exists
            if Path(expandedPath).exists():
                print(f"Found valid save path for '{game}': {expandedPath}")
                
                # Add or update the save path for the game in installedGames
                if game in installedGames:
                    installedGames[game]['save_path'] = expandedPath  # Update save_path
                else:
                    # If the game does not exist, create a new entry with save_path only
                    installedGames[game] = {"save_path": expandedPath}
                    
                if 'platform' not in installedGames[game] or not installedGames[game]['platform']:
                    installedGames[game]['platform'] = "General"  # Update platform only if not already set
            else:
                print(f"Save path does not exist for '{game}': {expandedPath}")

