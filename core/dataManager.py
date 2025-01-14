"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import json
from datetime import datetime
from modules.detectSystem import DetectSystem
from core.pathManager import PathManager

class DataManager:
    def __init__(self):
        self.PATH_steamLibrary = ""
        self.DATA_STEAM_library = ""
        
        self.DATA_EPIC_library = ""
        self.PATH_steamExe = ""
        self.PATH_epicLibrary = ""
        
        self.DATA_GEN_library = ""
        
        self.FOLDER_Data = "data"
        self.FOLDER_SaveGames = f"{self.FOLDER_Data}/savegames"
        self.FOLDER_Paths = f"{self.FOLDER_Data}/paths"
        
        self.URL_SteamAppIDs = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        self.STEAM_registryKey = r"SOFTWARE\Valve\Steam"
        self.EPIC_registryKey = r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher"
        
        self.PATH_APPID = f"{self.FOLDER_Data}/appid.json"
        self.pathInstalledGames = f"{self.FOLDER_Data}/installedGames.json"
        self.PATH_knownGamePaths = f"{self.FOLDER_Data}/knownGamePaths.json"
        self.PATH_customGames = f"{self.FOLDER_Data}/customGames.json"
        
        self.DATA_JSONinstalledGames = ""
        self.DATA_JSONknownGamePaths = ""
        self.DATA_JSONcustomGames = ""
        
        self.GITHUB_VERSION = "Version 0.9.9-alpha"
        self.GITHUB_DATE = datetime.now().strftime("%d-%m-%Y")
        self.GITHUB_ORIGIN = "JulianStiebler"
        self.GITHUB_PROJECT = "GameSaveVault"
        self.GITHUB_ASSIGNEES = "JulianStiebler"
        
        self.WINDOW_SIZE_X = 1000
        self.WINDOW_SIZE_Y = 800
        self.WINDOW_GEOMETRY = f"{self.WINDOW_SIZE_X}x{self.WINDOW_SIZE_Y}"
        self.WINDOW_STYLE = "darkly"
        self.WINDOW_TITLE = "Game Save Vault"
        self.URL_GitHub = f"https://github.com/{self.GITHUB_ORIGIN}/{self.GITHUB_PROJECT}/tree/main"
        self.URL_GitHub_FeatureRequest = f"https://github.com/{self.GITHUB_ORIGIN}/{self.GITHUB_PROJECT}/issues/new?assignees={self.GITHUB_ASSIGNEES}&labels=feature&projects=&template=feature_request.md&title=Feature+request"
        self.URL_GitHub_BugReport = f"https://github.com/{self.GITHUB_ORIGIN}/{self.GITHUB_PROJECT}/issues/new?assignees={self.GITHUB_ASSIGNEES}&labels=bug&projects=&template=bug_report.md&title=Bug+report"

        self.detectSystem = DetectSystem(self)

    def initApplication(self):
        self.DATA_JSONinstalledGames = self.loadJSON(self.pathInstalledGames, convertRelativePaths=True)
        self.DATA_JSONknownGamePaths = self.loadJSON(self.PATH_knownGamePaths)
        self.DATA_JSONcustomGames = self.loadJSON(self.PATH_customGames)

    @staticmethod
    def loadJSON(filePath, convertRelativePaths=False):
        """
        Load JSON data from a file.
        
        Args:
            filePath (str): Path to the JSON file
            convertRelativePaths (bool): Convert relative paths to absolute if True
        
        Returns:
            dict: Parsed JSON data with converted paths if specified
        """
        try:
            with open(filePath, 'r') as f:
                data = json.load(f)
                
                if convertRelativePaths and "installedGames" in filePath:
                    # Convert paths to absolute for in-memory use
                    for game_data in data.values():
                        if 'pathSave' in game_data:
                            game_data['pathSave'] = PathManager.path_expand(
                                game_data['pathSave'],
                                game_data.get('pathInstall')
                            )
                        if 'pathInstall' in game_data:
                            game_data['pathInstall'] = PathManager.path_expand(
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
