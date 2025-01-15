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

Last Edited: 11.01.2025
"""

import requests
import json
import os
import winreg

from core.enums import RegistryKeys, DataFile, PublicSources

class DetectGamesSteam:
    def __init__(self, data):
        self.data = data
    
    @staticmethod
    def GetAppIDList():
        response = requests.get(PublicSources.STEAM_APPLIST.value)

        if response.status_code == 200:
            data = response.json()
            
            # Sort apps by appid
            apps = sorted(data['applist']['apps'], key=lambda x: x['appid'])
            
            # Create a dictionary where appid is the key and name is the value
            output = {str(app['appid']): app['name'] for app in apps}
            
            with open(DataFile.APPID.value, 'w') as file:
                json.dump({'steamAppIDList': output}, file, indent=4)
        else:
            print(f"Error fetching API data. Status Code: {response.status_code}")

    def GetInstallPath(self):
        try:
            registryKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RegistryKeys.STEAM.value)
            steamPath, _ = winreg.QueryValueEx(registryKey, "SteamPath")
            return steamPath
        except FileNotFoundError:
            print("Steam path not found in the registry.")
            return None

    def GetLibraryPath(self):
        libraryFolderPath = os.path.join(self.data.PATH_steamExe, "steamapps", "libraryfolders.vdf")

        if not os.path.exists(libraryFolderPath):
            print(f"libraryfolders.vdf not found in {self.data.PATH_steamExe}.")
            return []

        # Read and parse the VDF file manually (as a normal text file)
        libraryPaths = []
        with open(libraryFolderPath, 'r', encoding='utf-8') as file:
            data = file.read()

        # Extract library paths from the "path" key
        for line in data.splitlines():
            if '"path"' in line:
                parts = line.split('"')
                if len(parts) > 3:
                    path = parts[3].strip()
                    libraryPaths.append(path)

        return libraryPaths

    def GetInstalledGames(self):
        def helper_ParseACFFile(ACFFilePath):
            gameDetails = {}
            
            try:
                with open(ACFFilePath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                for i, line in enumerate(lines):
                    if '"appid"' in line:
                        gameDetails['appid'] = line.split('"')[3]
                    elif '"name"' in line:
                        gameDetails['name'] = line.split('"')[3]
                    elif '"installdir"' in line:
                        gameDetails['installdir'] = line.split('"')[3]

            except Exception as e:
                print(f"Error reading {ACFFilePath}: {e}")

            return gameDetails
        
        # Check if the output file already exists and load the existing data
        if os.path.exists(DataFile.INSTALLED_GAMES.value):
            with open(DataFile.INSTALLED_GAMES.value, 'r', encoding='utf-8') as file:
                installedGames = json.load(file)
        else:
            installedGames = {}

        for paths in self.data.PATH_steamLibrary:
            steamAppsPaths = os.path.join(paths, "steamapps")

            # Check if the steamapps folder exists
            if not os.path.isdir(steamAppsPaths):
                print(f"steamapps folder not found in {paths}.")
                continue

            # Look for .acf files
            for ACFFile in os.listdir(steamAppsPaths):
                if ACFFile.endswith(".acf"):
                    ACFFilePath = os.path.join(steamAppsPaths, ACFFile)
                    gameDetails = helper_ParseACFFile(ACFFilePath)

                    if gameDetails:
                        # Ensure we preserve the game name if already exists
                        gameName = gameDetails.get("name")

                        # Determine the full install path
                        installDir = gameDetails.get('installdir')
                        if installDir:
                            if os.path.isabs(installDir):
                                gameDetails['pathInstall'] = os.path.normpath(installDir)
                            else:
                                gameDetails['pathInstall'] = os.path.normpath(os.path.join(paths, "steamapps", "common", installDir))

                            # If game already exists, update only non-existing fields, preserving pathSave if exists
                            if gameName in installedGames:
                                if 'pathSave' in installedGames[gameName]:
                                    gameDetails['pathSave'] = installedGames[gameName]['pathSave']
                                # Update only fields that are not present
                                installedGames[gameName].update({
                                    'appid': gameDetails['appid'],
                                    'pathInstall': gameDetails['pathInstall'],
                                    'installdir': gameDetails['installdir'],
                                    'name': gameName  # Add name if not already present
                                })
                            else:
                                # If the game is new, add all the data
                                installedGames[gameName] = gameDetails
        return installedGames


