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

Last Edited: 16.01.2025
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog
import os
from datetime import datetime

from core.model import PathInfo
from core.enums import DataFolder, PathType

class Details:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        
        self.selectedBackup = ""
        
        self.LBL_gameTitle = ttk.Label(self.app.FRAME_details, text="Select a game", font=("Arial", 16, "bold"), anchor="center", bootstyle="light")
        self.LBL_gameTitle.pack(pady=10)
        self.LBL_installPath = ttk.Label(
            self.app.FRAME_details, 
            text="", 
            font=("Arial", 12), 
            anchor="w", 
            bootstyle="secondary",
            wraplength=500,  # Wrap text after 500 pixels
            justify="left"
        )
        self.LBL_installPath.pack(fill=X, padx=5, pady=2)

        self.LBL_savePath = ttk.Label(
            self.app.FRAME_details, 
            text="", 
            font=("Arial", 12), 
            anchor="w", 
            bootstyle="secondary",
            wraplength=500,  # Wrap text after 500 pixels
            justify="left"
        )
        self.LBL_savePath.pack(fill=X, padx=5, pady=2)

        self.FRAME_buttons = ttk.Frame(self.app.FRAME_details)
        self.FRAME_buttons.pack(fill=X, pady=5)
        
        # Add progress bar above backup buttons
        self.PROG_backupProgress = ttk.Progressbar(
            self.app.FRAME_details,
            mode='determinate',
            bootstyle="info"
        )

        self.BTN_openInstallPath = ttk.Button(self.app.FRAME_details, text="Open Installation Folder", command=self.__openInstallationFolder, bootstyle="outline-success")
        self.BTN_openInstallPath.pack(fill=X, padx=5, pady=2)
        self.BTN_openSavePath = ttk.Button(self.app.FRAME_details, text="Open Save Path Folder", command=self.__openSaveFolder, bootstyle="outline-danger")
        self.BTN_openSavePath.pack(fill=X, padx=5, pady=2)
        self.BTN_setInstallPath = ttk.Button(self.FRAME_buttons, text="Manually Set Installation Path", command=self.__setInstallPath, bootstyle="success")
        self.BTN_setInstallPath.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_setSavePath = ttk.Button(self.FRAME_buttons, text="Manually Set Save Path", command=self.__setSavePath, bootstyle="primary")
        self.BTN_setSavePath.pack(side=LEFT, expand=True, padx=5, pady=5)
        
        self.LIST_savePathContent = ttk.Treeview(self.app.FRAME_details, columns=["Filename", "Modified Date"], show="headings", bootstyle="dark")
        self.LIST_savePathContent.heading("Filename", text="Filename")
        self.LIST_savePathContent.heading("Modified Date", text="Modified Date")
        self.LIST_savePathContent.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.LIST_backupContents = ttk.Treeview(self.app.FRAME_details, show='tree', bootstyle="dark")
        self.LIST_backupContents.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        self.FRAME_backupButtons = ttk.Frame(self.app.FRAME_details)

        self.BTN_createBackup = ttk.Button(self.FRAME_backupButtons, text="Create Timestamped Backup", bootstyle="primary", command=self.app.backupManager.create)
        self.BTN_createBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_createBackup = ttk.Button(self.FRAME_backupButtons, text="Create Named Backup", bootstyle="primary", 
                                   command=lambda: self.app.backupManager.create(isNamed=True))
        self.BTN_createBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_applyBackup = ttk.Button(self.FRAME_backupButtons, text="Apply Backup", bootstyle="danger", 
                                    command=lambda: self.app.backupManager.apply(self.__getSelectedBackup()))
        self.BTN_applyBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.PROG_backupProgress['value'] = 0
        self.PROG_backupProgress.pack(fill=X, padx=5, pady=5)

        self.FRAME_backupButtons.pack(fill=X, pady=5)
        
    def updateDetailsView(self):
        installPath = self.data.DATA_JSONinstalledGames.get(self.app.selectedGameToDisplay.metadata.name, {}).get("pathInstall", None)
        savePath = self.data.DATA_JSONinstalledGames.get(self.app.selectedGameToDisplay.metadata.name, {}).get("pathSave", None)
        knownSavePath = self.data.DATA_JSONknownGamePaths.get(self.app.selectedGameToDisplay.metadata.name, "Unknown Path")
        

        self.LBL_installPath.config(text=f"Installation Folder: {PathInfo.to_relative(installPath)}" if installPath else "Installation folder not found.")
        self.LBL_savePath.config(text=f"Save Path: {PathInfo.to_relative(savePath)}" if savePath else f"Default Save Path: {knownSavePath}")

        self.BTN_openInstallPath.config(state=NORMAL if installPath else DISABLED)
        self.BTN_openSavePath.config(state=NORMAL if savePath else DISABLED)
        
    def updateLIST_fileExplorer(self):
        for item in self.LIST_savePathContent.get_children():
            self.LIST_savePathContent.delete(item)

        savePath = self.data.DATA_JSONinstalledGames.get(self.app.selectedGameToDisplay.metadata.name, {}).get("pathSave", None)
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
        sanitizedGameName = self.data.utility.sanitizeFolderName_fix(self.app.selectedGameToDisplay.metadata.name)
        backupFolder = os.path.join(DataFolder.SAVEGAMES.value, sanitizedGameName)
        
        if os.path.exists(backupFolder):
            for file in os.listdir(backupFolder):
                if file.endswith(".zip"):
                    self.LIST_backupContents.insert("", "end", text=file)

        # Adjust the height of the Treeview
        self.data.utility.adjustTreeviewHeight(self.LIST_backupContents)
            
    def __getSelectedBackup(self):
        selected = self.LIST_backupContents.selection()
        if selected:
            self.selectedBackup = self.LIST_backupContents.item(selected[0], "text")
            return self.selectedBackup
        else:
            # Handle case where no item is selected, return an empty string or raise an error
            return ""

    def __openInstallationFolder(self):
        installPath = self.data.DATA_JSONinstalledGames[self.app.selectedGameToDisplay.metadata.name].get("pathInstall", None)
        if installPath:
            self.data.utility.openFolderInExplorer(installPath)

    def __openSaveFolder(self):
        savePath = self.data.DATA_JSONinstalledGames[self.app.selectedGameToDisplay.metadata.name].get("pathSave", None)
        if savePath:
            self.data.utility.openFolderInExplorer(savePath)
            
    def __setInstallPath(self):
        folder = filedialog.askdirectory(title="Select Installation Folder")
        if folder:
            self.data.DATA_JSONinstalledGames.setdefault(self.app.selectedGameToDisplay.metadata.name, {})["pathInstall"] = folder
            self.app.updatePaths()
            self.data.saveJSON(self.data.PATH_JSONinstalledGames, self.data.DATA_JSONinstalledGames)

    def __setSavePath(self):
        folder = filedialog.askdirectory(title="Select Save Path Folder")
        if folder:
            self.data.DATA_JSONinstalledGames.setdefault(self.app.selectedGameToDisplay.metadata.name, {})["pathSave"] = folder
            self.app.updatePaths()
            self.app.updateSaveFolderContents()
            self.data.saveJSON(self.data.PATH_JSONinstalledGames, self.data.DATA_JSONinstalledGames)