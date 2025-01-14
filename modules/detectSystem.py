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
        self.pathManager = PathManager(self.data)
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
            if 'pathInstall' in game_data:
                game_data['pathInstall'] = self.pathManager.path_make_relative(game_data['pathInstall'])
            if 'pathSave' in game_data:
                game_data['pathSave'] = self.pathManager.path_make_relative(game_data['pathSave'])
            
            # Update or create entry
            if game_name in self.installedGames:
                # Keep existing platform if it's Steam or Epic
                game_data['platform'] = platform
                
                # Preserve existing save_path if present
                if 'pathSave' in self.installedGames[game_name]:
                    game_data['pathSave'] = self.installedGames[game_name]['pathSave']
                
                # Update existing entry
                self.installedGames[game_name].update(game_data)
            else:
                # Create new entry
                game_data['platform'] = platform
                self.installedGames[game_name] = game_data

        # Write updated data to file
        with open(self.data.pathInstalledGames, 'w') as f:
            json.dump(self.installedGames, f, indent=4)