import json
from .detectEpicGames import DetectGamesEpic
from .detectSteamGames import DetectGamesSteam
from .detectGeneralGames import DetectGamesGeneral
from core.pathManager import PathManager
from typing import Dict
from core.model import InstalledGame, KnownGamePath

class DetectSystem:
    def __init__(self, dataManager):
        self.data = dataManager
        self.pathManager = PathManager()
        self.detectEpic = DetectGamesEpic(self.data)
        self.detectSteam = DetectGamesSteam(self.data)
        self.detectGeneral = DetectGamesGeneral(self.data)
        self.installedGames: Dict[str, InstalledGame] = {}
        
    def initEpicLibrary(self):
        self.data.PATH_epicLibrary = self.detectEpic.GetInstallPath()
        self.data.DATA_EPIC_library = self.detectEpic.GetInstalledGames(self.data.PATH_epicLibrary)
        self.saveInstalledGames(self.data.DATA_EPIC_library, "Epic")

    def initSteamLibrary(self):
        self.detectSteam.GetAppIDList(self.data.URL_SteamAppIDs, self.data.PATH_APPID)
        self.data.PATH_steamExe = self.detectSteam.GetInstallPath()
        self.data.PATH_steamLibrary = self.detectSteam.GetLibraryPath()
        self.data.DATA_STEAM_library = self.detectSteam.GetInstalledGames()
        self.saveInstalledGames(self.data.DATA_STEAM_library, "Steam")

    def initGeneralLibrary(self):
        self.data.DATA_GEN_library = self.detectGeneral.GetSaveFolders()
        self.saveInstalledGames(self.data.DATA_GEN_library, "General")

    def saveInstalledGames(self, new_games: Dict[str, dict], platform: str = "General"):
        for game_name, game_data in new_games.items():
            # Convert paths to relative
            if 'path_install' in game_data:
                game_data['path_install'] = self.pathManager.path_make_relative(game_data['path_install'])
            if 'path_save' in game_data:
                game_data['path_save'] = self.pathManager.path_make_relative(game_data['path_save'])
            
            # Update or create entry
            if game_name in self.installedGames:
                # Keep existing platform if it's Steam or Epic
                game_data['platform'] = platform
                
                # Preserve existing save_path if present
                if 'path_save' in self.installedGames[game_name]:
                    game_data['path_save'] = self.installedGames[game_name]['path_save']
                
                # Update existing entry
                self.installedGames[game_name].update(game_data)
            else:
                # Create new entry
                game_data['platform'] = platform
                self.installedGames[game_name] = game_data

        # Write updated data to file
        with open(self.data.PATH_installedGames, 'w') as f:
            json.dump(self.installedGames, f, indent=4)