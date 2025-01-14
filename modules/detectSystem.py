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
        self.saveInstalledGames(self.data.DATA_EPIC_library)

    def initSteamLibrary(self):
        self.detectSteam.GetAppIDList(self.data.URL_SteamAppIDs, self.data.PATH_APPID)
        self.data.PATH_steamExe = self.detectSteam.GetInstallPath()
        self.data.PATH_steamLibrary = self.detectSteam.GetLibraryPath()
        self.data.DATA_STEAM_library = self.detectSteam.GetInstalledGames()
        self.saveInstalledGames(self.data.DATA_STEAM_library)

    def initGeneralLibrary(self):
        self.data.DATA_GEN_library = self.detectGeneral.GetSaveFolders()
        self.saveInstalledGames(self.data.DATA_GEN_library)

    def saveInstalledGames(self, installedGames: Dict[str, dict]):
        # Convert dictionary data to InstalledGame objects
        for gameName, gameData in installedGames.items():
            # Convert paths to relative before creating InstalledGame
            if 'path_install' in gameData:
                gameData['path_install'] = self.pathManager.make_relative(gameData['path_install'])
            if 'path_save' in gameData:
                gameData['path_save'] = self.pathManager.make_relative(gameData['path_save'])
                
            gameObject = InstalledGame.from_dict(gameData)
            self.installedGames[gameName] = gameObject.to_dict()

        # Save to file
        with open(self.data.PATH_installedGames, 'w') as f:
            json.dump(self.installedGames, f, indent=4)