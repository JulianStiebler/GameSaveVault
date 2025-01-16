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

import os
import json
from pathlib import Path
import json
import os

from core.enums import DataFile

class DetectGamesGeneral:
    def __init__(self):
        pass
        
    def GetSaveFolders(self):
        try:
            with open(DataFile.KNOWN_PATHS.value, 'r') as f:
                known_paths = json.load(f)
        except FileNotFoundError:
            print(f"Known game paths file not found: {DataFile.KNOWN_PATHS.value}")
            return {}

        try:
            with open(DataFile.INSTALLED_GAMES.value, 'r') as f:
                installedGames = json.load(f)
        except FileNotFoundError:
            installedGames = {}

        try:
            for gameName, path_data in known_paths.items():
                # Handle both string paths and complex objects
                pathSave = path_data.get('pathSave', path_data) if isinstance(path_data, dict) else path_data
                
                if "%gameinstall%" in pathSave:
                    if gameName in installedGames and 'pathInstall' in installedGames[gameName]:
                        pathInstall = installedGames[gameName]['pathInstall']
                        if pathInstall:
                            pathSave = pathSave.replace("%gameinstall%", pathInstall)
                    else:
                        print(f"Install path for '{gameName}' not found")
                        continue

                expanded_path = os.path.normpath(os.path.expandvars(pathSave))
                if Path(expanded_path).exists():
                    print(f"Found valid save path for '{gameName}': {expanded_path}")
                    if gameName in installedGames:
                        installedGames[gameName]['pathSave'] = pathSave  # Store original path
                    else:
                        installedGames[gameName] = {
                            "pathSave": pathSave  # Store original path
                        }
                else:
                    print(f"Save path does not exist: {expanded_path}")

            return installedGames
        except Exception as e:
            print(f"Error reading or parsing {DataFile.KNOWN_PATHS.value}: {e}")
            return {}

