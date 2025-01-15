import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from core.model import DataFile
import os
from gui.screen.dialog import AddMissingGameDialog
from tkinter import messagebox

class ListGames:
    def __init__(self, root, data, utility, app):
        self.root = root
        self.data = data
        self.utility = utility
        self.app = app

        self.BTN_addMissingGame = ttk.Button(self.app.FRAME_left, text="Add Missing Game", bootstyle="info", command=self.__addMissingGame)
        self.BTN_addMissingGame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # Button at the bottom
        self.LIST_games = ttk.Treeview(self.app.FRAME_left, show='tree', selectmode='browse', bootstyle="info")
        self.LIST_games.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Grid for Treeview to expand
        self.LIST_games.bind("<<TreeviewSelect>>", self.app.onGameSelect)

        # Scrollbar for the Treeview
        self.LIST_games_scrollbar = ttk.Scrollbar(self.app.FRAME_left, orient=VERTICAL, command=self.LIST_games.yview, bootstyle="danger")
        self.LIST_games_scrollbar.grid(row=0, column=1, sticky="ns")  # Place scrollbar in the same row as Treeview, stretching vertically

        # Configure grid to make the Treeview expand properly
        self.app.FRAME_left.grid_rowconfigure(0, weight=1)  # Row 0 (Treeview) expands to fill the space
        self.app.FRAME_left.grid_columnconfigure(0, weight=1)  # Column 0 (Treeview) expands to fill the space

        # Configure the Treeview to use the scrollbar
        self.LIST_games.configure(yscrollcommand=self.LIST_games_scrollbar.set)
        
    def __addMissingGame(self):
        dialog = AddMissingGameDialog(self.root, self.data)
        result = dialog.result

        if not result:
            return

        gameName = result["name"]
        savePath = result.get("savePath")
        installPath = result.get("installPath")
        isInstalled = result["isInstalled"]

        # Update customGames.json
        customGames = self.data.loadJSON(DataFile.CUSTOM_GAMES.value) if os.path.exists(DataFile.CUSTOM_GAMES.value) else {"CustomPaths": {}}
        customGames["CustomPaths"][gameName] = savePath or ""
        self.data.saveJSON(DataFile.CUSTOM_GAMES.value, customGames)

        # Update installedGames.json if the game is installed
        if isInstalled:
            installedGames = self.data.loadJSON(DataFile.INSTALLED_GAMES.value) if os.path.exists(DataFile.INSTALLED_GAMES.value) else {}
            installedGames[gameName] = {
                "platform": "Custom",
                **({"pathInstall": installPath} if installPath else {}),
                **({"pathSave": savePath} if savePath else {})
            }
            self.data.saveJSON(DataFile.INSTALLED_GAMES.value, installedGames)

        messagebox.showinfo("Success", f"Game '{gameName}' added successfully!")
        
    def populateLIST_games(self):
        self.gameList = []
        installedGameNames = {game.lower() for game in self.data.DATA_JSONinstalledGames.keys()}  # Get all installed game names (case-insensitive)

        # Add installed games first, sorted alphabetically
        installedGames = sorted(
            [(game, True) for game in self.data.DATA_JSONinstalledGames.keys()],
            key=lambda x: x[0].lower()  # Sorting by the game name (case-insensitive)
        )
        self.gameList.extend(installedGames)

        # Add known games only if not already in installed games, sorted alphabetically
        knownGames = sorted(
            [(game, False) for game, path in self.data.DATA_JSONknownGamePaths.items() if game.lower() not in installedGameNames],
            key=lambda x: x[0].lower()  # Sorting by the game name (case-insensitive)
        )
        self.gameList.extend(knownGames)
        self.updateLIST_games()
        
    def updateLIST_games(self, *args):
        searchTerm = self.app.searchVar.get().lower()
        for item in self.LIST_games.get_children():
            self.LIST_games.delete(item)

        sortedGames = sorted(self.gameList, key=lambda x: not x[1])
        for game, is_installed in sortedGames:
            if searchTerm in game.lower():
                status = "\u2713" if is_installed else "\u2717"
                self.LIST_games.insert("", "end", text=f"{status} {game}")