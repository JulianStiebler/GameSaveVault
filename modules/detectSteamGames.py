"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import requests
import json
import os
import winreg

class DetectGamesSteam:
    @staticmethod
    def GetAppIDList(url, outputFile):
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            
            # Sort apps by appid
            apps = sorted(data['applist']['apps'], key=lambda x: x['appid'])
            
            # Create a dictionary where appid is the key and name is the value
            output = {str(app['appid']): app['name'] for app in apps}
            
            with open(outputFile, 'w') as file:
                json.dump({'steamAppIDList': output}, file, indent=4)
        else:
            print(f"Error fetching API data. Status Code: {response.status_code}")

    @staticmethod
    def GetInstallPath(regKey):
        try:
            registryKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, regKey)
            steamPath, _ = winreg.QueryValueEx(registryKey, "SteamPath")
            return steamPath
        except FileNotFoundError:
            print("Steam path not found in the registry.")
            return None

    @staticmethod
    def GetLibraryPath(steamPath):
        libraryFolderPath = os.path.join(steamPath, "steamapps", "libraryfolders.vdf")

        if not os.path.exists(libraryFolderPath):
            print(f"libraryfolders.vdf not found in {steamPath}.")
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

    @staticmethod
    def GetInstalledGames(libraryPath, outputFile):
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
        if os.path.exists(outputFile):
            with open(outputFile, 'r', encoding='utf-8') as file:
                installedGames = json.load(file)
        else:
            installedGames = {}

        for paths in libraryPath:
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
                                gameDetails['install_path'] = os.path.normpath(installDir)
                            else:
                                gameDetails['install_path'] = os.path.normpath(os.path.join(paths, "steamapps", "common", installDir))

                            # If game already exists, update only non-existing fields, preserving save_path if exists
                            if gameName in installedGames:
                                if installedGames[gameName].get('platform', "") in ["General", ""]:
                                    installedGames[gameName]['platform'] = "Steam"
                                if 'save_path' in installedGames[gameName]:
                                    gameDetails['save_path'] = installedGames[gameName]['save_path']
                                # Update only fields that are not present
                                installedGames[gameName].update({
                                    'appid': gameDetails['appid'],
                                    'install_path': gameDetails['install_path'],
                                    'installdir': gameDetails['installdir'],
                                    'name': gameName  # Add name if not already present
                                })
                            else:
                                # If the game is new, add all the data
                                installedGames[gameName] = gameDetails

        # Write the updated games data back to the output file
        with open(outputFile, 'w', encoding='utf-8') as file:
            json.dump(installedGames, file, indent=4)
        print(f"\nInstalled games saved to {outputFile}.")
        return installedGames


