import json
from .detectEpicGames import DetectGamesEpic
from .detectSteamGames import DetectGamesSteam
from .detectGeneralGames import DetectGamesGeneral

class DetectSystem:
    def __init__(self, dataManager):
        self.data = dataManager
        self.detectEpic = DetectGamesEpic(self.data)
        self.detectSteam = DetectGamesSteam(self.data)
        self.detectGeneral = DetectGamesGeneral(self.data)
        self.installedGames = {}
        
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

    def saveInstalledGames(self, data):
        try:
            self.installedGames.update(data)
            with open(self.data.PATH_installedGames, 'w') as f:
                json.dump(self.installedGames, f, indent=4)
        except Exception as e:
            print(f"Error saving installed games: {e}")