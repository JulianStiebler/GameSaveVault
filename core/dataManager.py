"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import json
from datetime import datetime
from modules.detectEpicGames import DetectGamesEpic
from modules.detectSteamGames import DetectGamesSteam
from modules.detectGeneralGames import DetectGamesGeneral

class DataManger:
    def __init__(self):
        self.PATH_steamLibrary = ""
        self.PATH_steamExe = ""
        self.PATH_epicLibrary = ""
        
        self.FOLDER_Data = "data"
        self.FOLDER_SaveGames = f"{self.FOLDER_Data}/savegames"
        self.FOLDER_Paths = f"{self.FOLDER_Data}/paths"
        
        self.URL_SteamAppIDs = "https://api.steampowered.com/ISteamApps/GetAppList/v2/"
        self.REGISTRY_STEAM = r"SOFTWARE\Valve\Steam"
        self.REGISTRY_EPIC = r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher"
        
        self.PATH_KNOWNPATHS = f"{self.FOLDER_Data}/knownGamePaths.json"
        self.PATH_APPID = f"{self.FOLDER_Data}/appid.json"
        self.PATH_installedGames = f"{self.FOLDER_Data}/installedGames.json"
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

        self.detectEpic = DetectGamesEpic()
        self.detectSteam = DetectGamesSteam()
        self.detectGames = DetectGamesGeneral()
        
    def initSteamLibrary(self):
        self.detectSteam.GetAppIDList(self.URL_SteamAppIDs, self.PATH_APPID)
        self.PATH_steamExe = self.detectSteam.GetInstallPath(self.REGISTRY_STEAM)
        self.PATH_steamLibrary = self.detectSteam.GetLibraryPath(self.PATH_steamExe)
        self.detectSteam.GetInstalledGames(self.PATH_steamLibrary, self.PATH_installedGames)

    def initEpicLibrary(self):
        self.PATH_epicLibrary = self.detectEpic.GetInstallPath(self.REGISTRY_EPIC)
        self.detectEpic.GetInstalledGames(self.PATH_epicLibrary, self.PATH_installedGames)

    def initGeneralLibrary(self):
        self.detectGames.GetSaveFolders(self.PATH_knownGamePaths, self.PATH_installedGames)

    def initApplication(self):
        self.DATA_JSONinstalledGames = self.loadJSON(self.PATH_installedGames)
        self.DATA_JSONknownGamePaths = self.loadJSON(self.PATH_knownGamePaths)
        self.DATA_JSONcustomGames = self.loadJSON(self.PATH_customGames)

    @staticmethod
    def loadJSON(filePath):
        """
        Load JSON data from a file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            dict: The parsed JSON data, or an empty dictionary if the file does not exist or cannot be loaded.
        """
        try:
            with open(filePath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File not found: {filePath}")
            return {}  # Return an empty dictionary if the file doesn't exist
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {filePath}: {e}")
            return {}  # Return an empty dictionary if JSON is malformed
        except Exception as e:
            print(f"Unexpected error reading file {filePath}: {e}")
            return {}  # Return an empty dictionary for any other errors
        
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
