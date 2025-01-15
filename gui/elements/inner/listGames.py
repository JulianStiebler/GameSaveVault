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

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
from tkinter import messagebox

from core.model import DataFile
from gui.screen.dialog import AddMissingGameDialog

class ListGames:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app

        self.BTN_addMissingGame = ttk.Button(self.app.FRAME_left, text="Add Missing Game", bootstyle="info", command=self.__addMissingGame)
        self.BTN_addMissingGame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # Button at the bottom
        self.listGames = ttk.Treeview(self.app.FRAME_left, show='tree', selectmode='browse', bootstyle="info")
        self.listGames.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Grid for Treeview to expand
        self.listGames.bind("<<TreeviewSelect>>", self.app.onGameSelect)

        # Scrollbar for the Treeview
        self.listGames_scrollbar = ttk.Scrollbar(self.app.FRAME_left, orient=VERTICAL, command=self.listGames.yview, bootstyle="danger")
        self.listGames_scrollbar.grid(row=0, column=1, sticky="ns")  # Place scrollbar in the same row as Treeview, stretching vertically

        # Configure grid to make the Treeview expand properly
        self.app.FRAME_left.grid_rowconfigure(0, weight=1)  # Row 0 (Treeview) expands to fill the space
        self.app.FRAME_left.grid_columnconfigure(0, weight=1)  # Column 0 (Treeview) expands to fill the space

        # Configure the Treeview to use the scrollbar
        self.listGames.configure(yscrollcommand=self.listGames_scrollbar.set)
        
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
        self.populate()
        
    def populate(self):
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
        self.update()
        
    def update(self, *args):
        searchTerm = self.app.searchVar.get().lower()
        for item in self.listGames.get_children():
            self.listGames.delete(item)

        sortedGames = sorted(self.gameList, key=lambda x: not x[1])
        for game, is_installed in sortedGames:
            if searchTerm in game.lower():
                status = "\u2713" if is_installed else "\u2717"
                self.listGames.insert("", "end", text=f"{status} {game}")