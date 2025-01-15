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
from datetime import datetime
from tkinter import filedialog

from core import DataManager, BackupManager
from core.model import PathInfo
from core.enums import AppConfig, DataFolder
from gui.elements import Footer, Details, SearchBar, SideBar, ContextMenu

data = DataManager()

class GameSaveVault:
    def __init__(self, root, data):
        # ------------------------------------------ Application Init ------------------------------------------
        self.root = root
        self.data = data
        self.root.title(AppConfig.WINDOW_TITLE.value)
        self.root.geometry(AppConfig.WINDOW_GEOMETRY.value)
        self.root.minsize(AppConfig.WINDOW_SIZE_X.value, AppConfig.WINDOW_SIZE_Y.value)
        self.style = ttk.Style(AppConfig.WINDOW_THEME.value)
        self.backupManager = BackupManager(self.root, self.data, self)
    
        
        # ------------------------------------------ Runtime Variables ------------------------------------------
        self.selectedGameToDisplayDetails = None
        self.searchVar = ttk.StringVar()
        
        # ------------------------------------------ GUI Initialization ------------------------------------------
        self.FRAME_top = ttk.Frame(self.root)
        self.ELEM_contextMenu = ContextMenu(self.root, self.data, self)
        self.ELEM_searchBar = SearchBar(self.root, self.data, self)
        self.FRAME_top.pack(fill=ttk.X, padx=10, pady=10)
        
        self.FRAME_main = ttk.Panedwindow(self.root, orient=HORIZONTAL)
        self.FRAME_main.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.FRAME_left = ttk.Frame(self.FRAME_main)
        self.FRAME_main.add(self.FRAME_left, weight=1)
        self.ELEM_sideBar = SideBar(self.root, self.data, self)
        self.ELEM_sideBar.listGames.populate()

        self.FRAME_details = ttk.Frame(self.FRAME_main)
        self.FRAME_main.add(self.FRAME_details, weight=3)
        self.ELEM_details = Details(self.root, self.data, self)
        self.ELEM_footer = Footer(self.root, self.data, self)
        

        self.searchVar.trace_add("write", self.ELEM_sideBar.listGames.update)
        self.data.utility.adjustTreeviewHeight(self.ELEM_details.LIST_savePathContent)
        self.data.utility.adjustTreeviewHeight(self.ELEM_details.LIST_backupContents)
        
    def updateProgress(self, value):
        self.ELEM_details.PROG_backupProgress['value'] = value
        self.root.update_idletasks()
            
    def onGameSelect(self, event):
        selected = self.ELEM_sideBar.listGames.listGames.selection()
        if not selected:
            return

        gameName = self.ELEM_sideBar.listGames.listGames.item(selected[0], "text")[2:].strip()
        self.ELEM_details.LBL_gameTitle.config(text=gameName)
        self.selectedGameToDisplayDetails = gameName

        self.updateDetailsView()
        self.updateLIST_fileExplorer()
        self.updateLIST_backupContents()

    def updateDetailsView(self):
        installPath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("pathInstall", None)
        savePath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("pathSave", None)
        knownSavePath = self.data.DATA_JSONknownGamePaths.get(self.selectedGameToDisplayDetails, "Unknown Path")

        self.ELEM_details.LBL_installPath.config(text=f"Installation Folder: {PathInfo.to_relative(installPath)}" if installPath else "Installation folder not found.")
        self.ELEM_details.LBL_savePath.config(text=f"Save Path: {PathInfo.to_relative(savePath)}" if savePath else f"Default Save Path: {knownSavePath}")

        self.ELEM_details.BTN_openInstallPath.config(state=NORMAL if installPath else DISABLED)
        self.ELEM_details.BTN_openSavePath.config(state=NORMAL if savePath else DISABLED)

    def updateLIST_fileExplorer(self):
        for item in self.ELEM_details.LIST_savePathContent.get_children():
            self.ELEM_details.LIST_savePathContent.delete(item)

        savePath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("pathSave", None)
        if savePath and os.path.exists(savePath):
            for file in os.listdir(savePath):
                filePath = os.path.join(savePath, file)
                modifiedTime = datetime.fromtimestamp(os.path.getmtime(filePath)).strftime("%d-%m-%Y %H:%M:%S")
                self.ELEM_details.LIST_savePathContent.insert("", "end", values=(file, modifiedTime))

        # Adjust the height of the Treeview
        self.data.utility.adjustTreeviewHeight(self.ELEM_details.LIST_savePathContent)


    def updateLIST_backupContents(self):
        for item in self.ELEM_details.LIST_backupContents.get_children():
            self.ELEM_details.LIST_backupContents.delete(item)

        # Sanitize the selected game's name to ensure the folder name is valid
        sanitizedGameName = self.data.utility.sanitizeFolderName_fix(self.selectedGameToDisplayDetails)
        backupFolder = os.path.join(DataFolder.SAVEGAMES.value, sanitizedGameName)
        
        if os.path.exists(backupFolder):
            for file in os.listdir(backupFolder):
                if file.endswith(".zip"):
                    self.ELEM_details.LIST_backupContents.insert("", "end", text=file)

        # Adjust the height of the Treeview
        self.data.utility.adjustTreeviewHeight(self.ELEM_details.LIST_backupContents)
        
            
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    GameSaveVault(root)
    root.mainloop()
