"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import json
import os
import winreg

class DetectGamesEpic:
    def __init__(self, data):
        self.data = data

    def GetInstallPath(self):
        """Fetch the Epic Games installation path from the Windows registry."""
        try:
            # Open the Epic Games registry key
            registryKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.data.EPIC_registryKey)
            epicPath, _ = winreg.QueryValueEx(registryKey, "AppDataPath")
            return epicPath
        except FileNotFoundError:
            print("Epic Games registry path not found.")
            return None

    def GetInstalledGames(self, epicPath):
        """Fetch and save installed games from the LauncherInstalled.dat file."""
        if epicPath is None:
            print("Epic Games path is None.")
            return

        # Go back two folders from the epic_path
        basePath = os.path.abspath(os.path.join(epicPath, "..", ".."))
        
        # Path to the LauncherInstalled.dat file
        epicGamesInfoFile = os.path.join(basePath, "UnrealEngineLauncher", "LauncherInstalled.dat")
        
        if not os.path.exists(epicGamesInfoFile):
            print(f"LauncherInstalled.dat not found at {epicGamesInfoFile}.")
            return

        try:
            # Load existing installed games from the shared file
            if os.path.exists(self.data.PATH_installedGames):
                with open(self.data.PATH_installedGames, 'r', encoding='utf-8') as file:
                    installedGames = json.load(file)
            else:
                installedGames = {}

            # Open and load the JSON content from LauncherInstalled.dat
            with open(epicGamesInfoFile, 'r', encoding='utf-8') as file:
                data = json.load(file)

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
                        # Update platform only if it's not set or empty
                        if installedGames[gameName].get('platform', "") in ["General", ""]:
                            installedGames[gameName]['platform'] = "Epic"

                        installedGames[gameName].update({
                            "install_path": os.path.normpath(installLocation),
                        })
                    else:
                        installedGames[gameName] = {
                            "platform": "Epic",
                            "install_path": os.path.normpath(installLocation),
                        }

            return installedGames
        except Exception as e:
            print(f"Error reading or parsing {epicGamesInfoFile}: {e}")
            return {}

