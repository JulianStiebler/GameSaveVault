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

import os
from tkinter import messagebox
import shutil
from ttkbootstrap.constants import X
import zipfile

from core.enums import DataFolder
from gui.screen.dialog import NamedBackupDialog

invalidChars = r'[\/:*?"<>|]'
class BackupManager:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        
    def create(self, isNamed=False):
        sanitizedGameName = self.data.utility.sanitizeFolderName_fix(self.app.selectedGameToDisplayDetails)
        
        savePath = self.data.DATA_JSONinstalledGames[self.app.selectedGameToDisplayDetails].get("pathSave", "")
        backupFolder = os.path.join(DataFolder.SAVEGAMES.value, sanitizedGameName)
        os.makedirs(backupFolder, exist_ok=True)
        
        if not savePath:
            return
        
        if isNamed:
            # Prompt the user for a custom name
            zipName = NamedBackupDialog(self.root, self.data, self.data.utility, targetPath=backupFolder).result
            if not zipName:  # If the user cancels or leaves it empty, return
                return
        else:
            timestamp = self.data.getTimestamp()
            zipName = f"{sanitizedGameName}-{timestamp}.zip"
            
        zipPath = os.path.join(backupFolder, zipName)
        
        # Show and reset progress bar
        self.app.PROG_backupProgress.pack(fill=X, padx=5, pady=5)
        self.app.PROG_backupProgress['value'] = 0
        
        def __updateProgress(value):
            self.app.PROG_backupProgress['value'] = value
            self.root.update_idletasks()
        
        try:
            self.zipFolder(savePath, zipPath, __updateProgress)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
        finally:
            # Hide progress bar
            self.app.PROG_backupProgress.pack_forget()
        
        self.app.updateLIST_backupContents()
        messagebox.showinfo("Success", f"Backup '{zipName}' created successfully!")

    def apply(self):
        selected = self.app.LIST_backupContents.selection()
        if not selected:
            return

        zipFile = self.app.LIST_backupContents.item(selected[0], "text")
        
        # Sanitize the selected game name for folder paths, but not for zip files
        sanitizedGameName = self.data.utility.sanitizeFolderName_fix(self.app.selectedGameToDisplayDetails)
        backupFolder = os.path.join(DataFolder.SAVEGAMES.value, sanitizedGameName)
        zipPath = os.path.join(backupFolder, zipFile)

        savePath = self.data.DATA_JSONinstalledGames[self.app.selectedGameToDisplayDetails].get("pathSave", "")
        if os.path.exists(savePath):
            shutil.rmtree(savePath)
            
        os.makedirs(savePath, exist_ok=True)
        self.extractZIPContent(zipPath, savePath)
        self.app.updateLIST_backupContents()
        messagebox.showinfo("Success", f"Selected backup '{zipFile}' applied successfully!")
        

    @staticmethod
    def zipFolder(sourceFolder, zipFilePath, progressCallback=None):
        # Count total files first
        total_files = sum([len(files) for _, _, files in os.walk(sourceFolder)])
        current_file = 0
        
        with zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(sourceFolder):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, sourceFolder)
                    zipf.write(filepath, arcname)
                    current_file += 1
                    if progressCallback:
                        progress = (current_file / total_files) * 100
                        progressCallback(progress)

    @staticmethod
    def extractZIPContent(zipFilePath, targetFolder):
        with zipfile.ZipFile(zipFilePath, 'r') as zipf:
            os.makedirs(targetFolder, exist_ok=True)
            zipf.extractall(targetFolder)