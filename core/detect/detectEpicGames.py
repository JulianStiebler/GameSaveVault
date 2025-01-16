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
import os
import winreg
from typing import TYPE_CHECKING, Optional, Dict, List
from pathlib import Path
from core.enums import RegistryKeys, DataFile

class DetectGamesEpic:
    def __init__(self):
        self.epicPath: Optional[Path] = ""

    def GetInstallPath(self) -> Path | None:
        """Fetch the Epic Games installation path from the Windows registry."""
        try:
            # Open the Epic Games registry key
            registryKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, RegistryKeys.EPIC.value)
            self.epicPath, _ = winreg.QueryValueEx(registryKey, "AppDataPath")
            return self.epicPath
        except FileNotFoundError:
            print("Epic Games registry path not found.")
            return None

    def GetInstalledGames(self) -> Dict[str, Dict[str, Optional[str]]] | dict | None:
        """Fetch and save installed games from the LauncherInstalled.dat file."""
        if self.epicPath is None:
            print("Epic Games path is None.")
            return

        # Go back two folders from the epic_path
        basePath: str = os.path.abspath(os.path.join(self.epicPath, "..", ".."))
        # Path to the LauncherInstalled.dat file
        epicGamesInfoFile: str = os.path.join(basePath, "UnrealEngineLauncher", "LauncherInstalled.dat")
        
        if not os.path.exists(epicGamesInfoFile):
            print(f"LauncherInstalled.dat not found at {epicGamesInfoFile}.")
            return

        try:
            # Load existing installed games from the shared file
            if os.path.exists(DataFile.INSTALLED_GAMES.value):
                with open(DataFile.INSTALLED_GAMES.value, 'r', encoding='utf-8') as file:
                    installedGames: Dict[str, Dict[str, Optional[str]]] = json.load(file)
            else:
                installedGames: Dict[str, Dict[str, Optional[str]]] = {}

            # Open and load the JSON content from LauncherInstalled.dat
            with open(epicGamesInfoFile, 'r', encoding='utf-8') as file:
                data: Dict[str, List[Dict[str, str]]] = json.load(file)

            # Iterate over the installation list and filter out Unreal Engine related entries
            for app in data.get('InstallationList', []):
                appName = app.get("AppName")
                installLocation = app.get("InstallLocation")
                namespaceId = app.get("NamespaceId")

                # Skip Unreal Engine-related apps (NamespaceId = "ue")
                if namespaceId == "ue":
                    continue

                if appName and installLocation:
                    gameName = os.path.basename(installLocation)

                    # Add or update game entry with Epic-specific details
                    if gameName in installedGames:
                        installedGames[gameName].update({
                            "pathInstall": os.path.normpath(installLocation),
                        })
                    else:
                        installedGames[gameName] = {
                            "pathInstall": os.path.normpath(installLocation),
                        }

            return installedGames
        except Exception as e:
            print(f"Error reading or parsing {epicGamesInfoFile}: {e}")
            return {}

