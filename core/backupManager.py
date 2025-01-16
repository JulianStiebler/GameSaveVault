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
        sanitizedGameName = self.data.utility.sanitizeFolderName_fix(self.app.selectedGameToDisplay)
        
        savePath = self.data.DATA_JSONinstalledGames[self.app.selectedGameToDisplay].get("pathSave", "")
        backupFolder = os.path.join(DataFolder.SAVEGAMES.value, sanitizedGameName)
        os.makedirs(backupFolder, exist_ok=True)
        
        if not savePath:
            return
        
        if isNamed:
            # Prompt the user for a custom name
            zipName = NamedBackupDialog(self.root, self.data, backupFolder).result
            if not zipName:  # If the user cancels or leaves it empty, return
                return
        else:
            timestamp = self.data.getTimestamp()
            zipName = f"{sanitizedGameName}-{timestamp}.zip"
            
        zipPath = os.path.join(backupFolder, zipName)
        
        try:
            self.zipFolder(savePath, zipPath, self.app.updateProgress)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
        
        self.app.ELEM_details.updateLIST_backupContents()
        messagebox.showinfo("Success", f"Backup '{zipName}' created successfully!")

    def apply(self, selectedZip):
        if not selectedZip:
            messagebox.showerror("Error", "No backup selected.")
            return
        
        # Sanitize the selected game name for folder paths, but not for zip files
        sanitizedGameName = self.data.utility.sanitizeFolderName_fix(self.app.selectedGameToDisplay)
        backupFolder = os.path.join(DataFolder.SAVEGAMES.value, sanitizedGameName)
        zipPath = os.path.join(backupFolder, selectedZip)

        savePath = self.data.DATA_JSONinstalledGames[self.app.selectedGameToDisplay].get("pathSave", "")
        if os.path.exists(savePath):
            shutil.rmtree(savePath)
            
        os.makedirs(savePath, exist_ok=True)
        self.extractZIPContent(zipPath, savePath)
        self.app.ELEM_details.updateLIST_backupContents()
        messagebox.showinfo("Success", f"Selected backup '{selectedZip}' applied successfully!")
        

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