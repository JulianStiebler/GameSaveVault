import json
from .detectEpicGames import DetectGamesEpic
from .detectSteamGames import DetectGamesSteam
from .detectGeneralGames import DetectGamesGeneral
from typing import Dict
from core.enums import DataFile
from core.model import PathInfo

class DetectSystem:
    def __init__(self, dataManager):
        self.data = dataManager
        self.detectEpic = DetectGamesEpic(self.data)
        self.detectSteam = DetectGamesSteam(self.data)
        self.detectGeneral = DetectGamesGeneral(self.data)
        self.installedGames = {}
        
    def initEpicLibrary(self):
        self.data.PATH_epicLibrary = self.detectEpic.GetInstallPath()
        self.data.DATA_EPIC_library = self.detectEpic.GetInstalledGames()
        self.saveInstalledGames(self.data.DATA_EPIC_library, "Epic")

    def initSteamLibrary(self):
        self.detectSteam.GetAppIDList()
        self.data.PATH_steamExe = self.detectSteam.GetInstallPath()
        self.data.PATH_steamLibrary = self.detectSteam.GetLibraryPath()
        self.data.DATA_STEAM_library = self.detectSteam.GetInstalledGames()
        self.saveInstalledGames(self.data.DATA_STEAM_library, "Steam")

    def initGeneralLibrary(self):
        self.data.DATA_GEN_library = self.detectGeneral.GetSaveFolders()
        self.saveInstalledGames(self.data.DATA_GEN_library, "General")

    def saveInstalledGames(self, new_games: Dict[str, dict], platform):
        for game_name, game_data in new_games.items():
            # Convert paths to relative
            if 'pathInstall' in game_data:
                game_data['pathInstall'] = PathInfo.to_relative(game_data['pathInstall'])
            if 'pathSave' in game_data:
                game_data['pathSave'] = PathInfo.to_relative(game_data['pathSave'])
            if 'platform' in new_games[game_name]:
                game_data['platform'] = new_games[game_name]['platform']
            else:
                game_data['platform'] = platform

            
            # Update or create entry
            if game_name in self.installedGames:
                # Only write platform if it's missing (don't overwrite if it's already set)
                
                # Preserve existing save_path if present
                if 'pathSave' in self.installedGames[game_name]:
                    game_data['pathSave'] = self.installedGames[game_name]['pathSave']
                
                # Update existing entry
                self.installedGames[game_name].update(game_data)
            else:
                # Create new entry and assign the platform
                self.installedGames[game_name] = game_data

        # Write updated data to file
        with open(DataFile.INSTALLED_GAMES.value, 'w') as f:
            json.dump(self.installedGames, f, indent=4)