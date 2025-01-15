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

        self.__setupGUI_FrameRight()
        self.ELEM_details = Details(self.root, self.data, self)
        
        self.ELEM_footer = Footer(self.root, self.data, self)

        self.searchVar.trace_add("write", self.ELEM_sideBar.listGames.update)
        self.data.utility.adjustTreeviewHeight(self.LIST_savePathContent)
        self.data.utility.adjustTreeviewHeight(self.LIST_backupContents)
            
    def onGameSelect(self, event):
        selected = self.ELEM_sideBar.listGames.listGames.selection()
        if not selected:
            return

        gameName = self.ELEM_sideBar.listGames.listGames.item(selected[0], "text")[2:].strip()
        self.LBL_gameTitle.config(text=gameName)
        self.selectedGameToDisplayDetails = gameName

        self.updatePaths()
        self.updateSaveFolderContents()
        self.updateLIST_backupContents()

    def updatePaths(self):
        installPath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("pathInstall", None)
        savePath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("pathSave", None)
        knownSavePath = self.data.DATA_JSONknownGamePaths.get(self.selectedGameToDisplayDetails, "Unknown Path")

        self.LBL_installPath.config(text=f"Installation Folder: {PathInfo.to_relative(installPath)}" if installPath else "Installation folder not found.")
        self.LBL_savePath.config(text=f"Save Path: {PathInfo.to_relative(savePath)}" if savePath else f"Default Save Path: {knownSavePath}")

        self.BTN_openInstallPath.config(state=NORMAL if installPath else DISABLED)
        self.BTN_openSavePath.config(state=NORMAL if savePath else DISABLED)

    def updateSaveFolderContents(self):
        for item in self.LIST_savePathContent.get_children():
            self.LIST_savePathContent.delete(item)

        savePath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("pathSave", None)
        if savePath and os.path.exists(savePath):
            for file in os.listdir(savePath):
                filePath = os.path.join(savePath, file)
                modifiedTime = datetime.fromtimestamp(os.path.getmtime(filePath)).strftime("%d-%m-%Y %H:%M:%S")
                self.LIST_savePathContent.insert("", "end", values=(file, modifiedTime))

        # Adjust the height of the Treeview
        self.data.utility.adjustTreeviewHeight(self.LIST_savePathContent)


    def updateLIST_backupContents(self):
        for item in self.LIST_backupContents.get_children():
            self.LIST_backupContents.delete(item)

        # Sanitize the selected game's name to ensure the folder name is valid
        sanitizedGameName = self.data.utility.sanitizeFolderName_fix(self.selectedGameToDisplayDetails)
        backupFolder = os.path.join(DataFolder.SAVEGAMES.value, sanitizedGameName)
        
        if os.path.exists(backupFolder):
            for file in os.listdir(backupFolder):
                if file.endswith(".zip"):
                    self.LIST_backupContents.insert("", "end", text=file)

        # Adjust the height of the Treeview
        self.data.utility.adjustTreeviewHeight(self.LIST_backupContents)

    def __openInstallationFolder(self):
        installPath = self.data.DATA_JSONinstalledGames[self.selectedGameToDisplayDetails].get("pathInstall", None)
        if installPath:
            self.data.utility.openFolderInExplorer(installPath)

    def __openSaveFolder(self):
        savePath = self.data.DATA_JSONinstalledGames[self.selectedGameToDisplayDetails].get("pathSave", None)
        if savePath:
            self.data.utility.openFolderInExplorer(savePath)
            
    def __setInstallPath(self):
        folder = filedialog.askdirectory(title="Select Installation Folder")
        if folder:
            self.data.DATA_JSONinstalledGames.setdefault(self.selectedGameToDisplayDetails, {})["pathInstall"] = folder
            self.updatePaths()
            self.data.saveJSON(self.data.PATH_JSONinstalledGames, self.data.DATA_JSONinstalledGames)

    def __setSavePath(self):
        folder = filedialog.askdirectory(title="Select Save Path Folder")
        if folder:
            self.data.DATA_JSONinstalledGames.setdefault(self.selectedGameToDisplayDetails, {})["pathSave"] = folder
            self.updatePaths()
            self.updateSaveFolderContents()
            self.data.saveJSON(self.data.PATH_JSONinstalledGames, self.data.DATA_JSONinstalledGames)
            
        
    def __setupGUI_FrameRight(self):
        # Right panel for details
        self.FRAME_details = ttk.Frame(self.FRAME_main)
        self.FRAME_main.add(self.FRAME_details, weight=3)

        self.LBL_gameTitle = ttk.Label(self.FRAME_details, text="Select a game", font=("Arial", 16, "bold"), anchor="center", bootstyle="light")
        self.LBL_gameTitle.pack(pady=10)
        self.LBL_installPath = ttk.Label(
        self.FRAME_details, 
            text="", 
            font=("Arial", 12), 
            anchor="w", 
            bootstyle="secondary",
            wraplength=500,  # Wrap text after 500 pixels
            justify="left"
        )
        self.LBL_installPath.pack(fill=X, padx=5, pady=2)

        self.LBL_savePath = ttk.Label(
            self.FRAME_details, 
            text="", 
            font=("Arial", 12), 
            anchor="w", 
            bootstyle="secondary",
            wraplength=500,  # Wrap text after 500 pixels
            justify="left"
        )
        self.LBL_savePath.pack(fill=X, padx=5, pady=2)

        self.FRAME_buttons = ttk.Frame(self.FRAME_details)
        self.FRAME_buttons.pack(fill=X, pady=5)
        
        # Add progress bar above backup buttons
        self.PROG_backupProgress = ttk.Progressbar(
            self.FRAME_details,
            mode='determinate',
            bootstyle="info"
        )

        self.BTN_openInstallPath = ttk.Button(self.FRAME_details, text="Open Installation Folder", command=self.__openInstallationFolder, bootstyle="outline-success")
        self.BTN_openInstallPath.pack(fill=X, padx=5, pady=2)
        self.BTN_openSavePath = ttk.Button(self.FRAME_details, text="Open Save Path Folder", command=self.__openSaveFolder, bootstyle="outline-danger")
        self.BTN_openSavePath.pack(fill=X, padx=5, pady=2)
        self.BTN_setInstallPath = ttk.Button(self.FRAME_buttons, text="Manually Set Installation Path", command=self.__setInstallPath, bootstyle="success")
        self.BTN_setInstallPath.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_setSavePath = ttk.Button(self.FRAME_buttons, text="Manually Set Save Path", command=self.__setSavePath, bootstyle="primary")
        self.BTN_setSavePath.pack(side=LEFT, expand=True, padx=5, pady=5)

        # File list for save path contents
        self.LIST_savePathContent = ttk.Treeview(self.FRAME_details, columns=["Filename", "Modified Date"], show="headings", bootstyle="dark")
        self.LIST_savePathContent.heading("Filename", text="Filename")
        self.LIST_savePathContent.heading("Modified Date", text="Modified Date")
        self.LIST_savePathContent.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.LIST_backupContents = ttk.Treeview(self.FRAME_details, show='tree', bootstyle="dark")
        self.LIST_backupContents.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.FRAME_backupButtons = ttk.Frame(self.FRAME_details)

        self.BTN_createBackup = ttk.Button(self.FRAME_backupButtons, text="Create Timestamped Backup", bootstyle="primary", command=self.backupManager.create)
        self.BTN_createBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_createBackup = ttk.Button(self.FRAME_backupButtons, text="Create Named Backup", bootstyle="primary", 
                                   command=lambda: self.backupManager.create(isNamed=True))
        self.BTN_createBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_applyBackup = ttk.Button(self.FRAME_backupButtons, text="Apply Backup", bootstyle="danger", command=self.backupManager.apply)
        self.BTN_applyBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.PROG_backupProgress.pack(fill=X, padx=5, pady=5)

        self.FRAME_backupButtons.pack(fill=X, pady=5)
        
            
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    GameSaveVault(root)
    root.mainloop()
