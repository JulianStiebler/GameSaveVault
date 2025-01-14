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

class DetectGamesGeneral:
    def __init__(self, data):
        self.data = data
        
    def GetSaveFolders(self):
        try:
            with open(self.data.PATH_knownGamePaths, 'r') as f:
                known_paths = json.load(f)
        except FileNotFoundError:
            print(f"Known game paths file not found: {self.data.PATH_knownGamePaths}")
            return {}

        try:
            with open(self.data.PATH_installedGames, 'r') as f:
                installedGames = json.load(f)
        except FileNotFoundError:
            installedGames = {}

        for gameName, path_data in known_paths.items():
            # Handle both string paths and complex objects
            path_save = path_data.get('path_save', path_data) if isinstance(path_data, dict) else path_data
            
            if "%gameinstall%" in path_save:
                if gameName in installedGames and 'path_install' in installedGames[gameName]:
                    path_install = installedGames[gameName]['path_install']
                    if path_install:
                        path_save = path_save.replace("%gameinstall%", path_install)
                else:
                    print(f"Install path for '{gameName}' not found")
                    continue

            expanded_path = os.path.normpath(os.path.expandvars(path_save))
            if Path(expanded_path).exists():
                print(f"Found valid save path for '{gameName}': {expanded_path}")
                if gameName in installedGames:
                    installedGames[gameName]['path_save'] = path_save  # Store original path
                else:
                    installedGames[gameName] = {
                        "path_save": path_save  # Store original path
                    }
            else:
                print(f"Save path does not exist: {expanded_path}")

        return installedGames

