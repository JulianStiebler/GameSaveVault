"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import shutil
from datetime import datetime
from tkinter import filedialog, simpledialog, messagebox
from tkinter.messagebox import showinfo

from core.dataManager import DataManager
import core.util as util
from gui import Footer
from gui.screen.dialog import NamedBackupDialog, AddMissingGameDialog

data = DataManager()

class SaveFileManager:
    def __init__(self, root, data):
        self.root = root
        self.data = data if data else DataManager()
        self.root.title(self.data.WINDOW_TITLE)
        self.root.geometry(self.data.WINDOW_GEOMETRY)
        self.root.minsize(self.data.WINDOW_SIZE_X, self.data.WINDOW_SIZE_Y)
        self.style = ttk.Style(self.data.WINDOW_STYLE)
        self.selectedGameToDisplayDetails = None
        
        self.__setupGUI_searchBar()
        self.FRAME_main = ttk.Panedwindow(self.root, orient=HORIZONTAL)
        self.FRAME_main.pack(fill=BOTH, expand=True, padx=10, pady=10)
        

        self.__setupGUI_FrameLeft()
        self.__setupGUI_FrameRight()
        
        self.populateLIST_games()
        self.footer = Footer(self.root, self.data)
        
        util.adjustTreeviewHeight(self.LIST_savePathContent)
        util.adjustTreeviewHeight(self.LIST_backupContents)
            
    def onGameSelect(self, event):
        selected = self.LIST_games.selection()
        if not selected:
            return

        gameName = self.LIST_games.item(selected[0], "text")[2:].strip()
        self.LBL_gameTitle.config(text=gameName)
        self.selectedGameToDisplayDetails = gameName

        self.updatePaths()
        self.updateSaveFolderContents()
        self.updateLIST_backupContents()
        
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
        searchTerm = self.searchVar.get().lower()
        for item in self.LIST_games.get_children():
            self.LIST_games.delete(item)

        sortedGames = sorted(self.gameList, key=lambda x: not x[1])
        for game, is_installed in sortedGames:
            if searchTerm in game.lower():
                status = "\u2713" if is_installed else "\u2717"
                self.LIST_games.insert("", "end", text=f"{status} {game}")

    def updatePaths(self):
        installPath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("path_install", None)
        savePath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("path_save", None)
        knownSavePath = self.data.DATA_JSONknownGamePaths.get(self.selectedGameToDisplayDetails, "Unknown Path")

        self.LBL_installPath.config(text=f"Installation Folder: {installPath}" if installPath else "Installation folder not found.")
        self.LBL_savePath.config(text=f"Save Path: {savePath}" if savePath else f"Default Save Path: {knownSavePath}")

        self.BTN_openInstallPath.config(state=NORMAL if installPath else DISABLED)
        self.BTN_openSavePath.config(state=NORMAL if savePath else DISABLED)

    def updateSaveFolderContents(self):
        for item in self.LIST_savePathContent.get_children():
            self.LIST_savePathContent.delete(item)

        savePath = self.data.DATA_JSONinstalledGames.get(self.selectedGameToDisplayDetails, {}).get("path_save", None)
        if savePath and os.path.exists(savePath):
            for file in os.listdir(savePath):
                filePath = os.path.join(savePath, file)
                modifiedTime = datetime.fromtimestamp(os.path.getmtime(filePath)).strftime("%d-%m-%Y %H:%M:%S")
                self.LIST_savePathContent.insert("", "end", values=(file, modifiedTime))

        # Adjust the height of the Treeview
        util.adjustTreeviewHeight(self.LIST_savePathContent)


    def updateLIST_backupContents(self):
        for item in self.LIST_backupContents.get_children():
            self.LIST_backupContents.delete(item)

        # Sanitize the selected game's name to ensure the folder name is valid
        sanitizedGameName = util.sanitizeFolderName_fix(self.selectedGameToDisplayDetails)
        backupFolder = os.path.join(data.FOLDER_SaveGames, sanitizedGameName)
        
        if os.path.exists(backupFolder):
            for file in os.listdir(backupFolder):
                if file.endswith(".zip"):
                    self.LIST_backupContents.insert("", "end", text=file)

        # Adjust the height of the Treeview
        util.adjustTreeviewHeight(self.LIST_backupContents)


    def BackupCreate(self, isNamed=False):
        sanitizedGameName = util.sanitizeFolderName_fix(self.selectedGameToDisplayDetails)
        
        savePath = self.data.DATA_JSONinstalledGames[self.selectedGameToDisplayDetails].get("path_save", "")
        backupFolder = os.path.join(data.FOLDER_SaveGames, sanitizedGameName)
        os.makedirs(backupFolder, exist_ok=True)
        
        if not savePath:
            return
        
        if isNamed:
            # Prompt the user for a custom name
            zipName = NamedBackupDialog(self.root, self.data, targetPath=backupFolder).result
            if not zipName:  # If the user cancels or leaves it empty, return
                return
        else:
            timestamp = self.data.getTimestamp()
            zipName = f"{sanitizedGameName}-{timestamp}.zip"
            
        zipPath = os.path.join(backupFolder, zipName)
        
        # Show and reset progress bar
        self.PROG_backupProgress.pack(fill=X, padx=5, pady=5)
        self.PROG_backupProgress['value'] = 0
        
        def __updateProgress(value):
            self.PROG_backupProgress['value'] = value
            self.root.update_idletasks()
        
        try:
            util.zipFolder(savePath, zipPath, __updateProgress)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create backup: {str(e)}")
        finally:
            # Hide progress bar
            self.PROG_backupProgress.pack_forget()
        
        self.updateLIST_backupContents()
        messagebox.showinfo("Success", f"Backup '{zipName}' created successfully!")

    def BackupApply(self):
        selected = self.LIST_backupContents.selection()
        if not selected:
            return

        zipFile = self.LIST_backupContents.item(selected[0], "text")
        
        # Sanitize the selected game name for folder paths, but not for zip files
        sanitizedGameName = util.sanitizeFolderName_fix(self.selectedGameToDisplayDetails)
        backupFolder = os.path.join(data.FOLDER_SaveGames, sanitizedGameName)
        zipPath = os.path.join(backupFolder, zipFile)

        savePath = self.data.DATA_JSONinstalledGames[self.selectedGameToDisplayDetails].get("path_save", "")
        if savePath:
            shutil.rmtree(savePath)
            os.makedirs(savePath, exist_ok=True)
            util.extractZIPContent(zipPath, savePath)
        self.updateLIST_backupContents()
        messagebox.showinfo("Success", f"Selected backup '{zipFile}' applied successfully!")

    def __openInstallationFolder(self):
        installPath = self.data.DATA_JSONinstalledGames[self.selectedGameToDisplayDetails].get("path_install", None)
        if installPath:
            util.openFolderInExplorer(installPath)

    def __openSaveFolder(self):
        savePath = self.data.DATA_JSONinstalledGames[self.selectedGameToDisplayDetails].get("path_save", None)
        if savePath:
            util.openFolderInExplorer(savePath)
            
    def __setInstallPath(self):
        folder = filedialog.askdirectory(title="Select Installation Folder")
        if folder:
            self.data.DATA_JSONinstalledGames.setdefault(self.selectedGameToDisplayDetails, {})["path_install"] = folder
            self.updatePaths()
            self.data.saveJSON(self.data.PATH_JSONinstalledGames, self.data.DATA_JSONinstalledGames)

    def __setSavePath(self):
        folder = filedialog.askdirectory(title="Select Save Path Folder")
        if folder:
            self.data.DATA_JSONinstalledGames.setdefault(self.selectedGameToDisplayDetails, {})["path_save"] = folder
            self.updatePaths()
            self.updateSaveFolderContents()
            self.data.saveJSON(self.data.PATH_JSONinstalledGames, self.data.DATA_JSONinstalledGames)
            
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
        customGames = self.data.loadJSON(self.data.PATH_customGames) if os.path.exists(self.data.PATH_customGames) else {"CustomPaths": {}}
        customGames["CustomPaths"][gameName] = savePath or ""
        self.data.saveJSON(self.data.PATH_customGames, customGames)

        # Update installedGames.json if the game is installed
        if isInstalled:
            installedGames = self.data.loadJSON(self.data.PATH_installedGames) if os.path.exists(self.data.PATH_installedGames) else {}
            installedGames[gameName] = {
                "platform": "Custom",
                **({"path_install": installPath} if installPath else {}),
                **({"path_save": savePath} if savePath else {})
            }
            self.data.saveJSON(self.data.PATH_installedGames, installedGames)

        messagebox.showinfo("Success", f"Game '{gameName}' added successfully!")
        self.data.initApplication()
        self.populateLIST_games()
        
    def __setupGUI_searchBar(self):
        self.searchVar = ttk.StringVar()
        self.searchVar.trace_add("write", self.updateLIST_games)
        INP_SearchBar = ttk.Entry(self.root, textvariable=self.searchVar, font=("Arial", 14))
        INP_SearchBar.pack(fill=X, padx=10, pady=5)
        
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

        self.BTN_createBackup = ttk.Button(self.FRAME_backupButtons, text="Create Timestamped Backup", bootstyle="primary", command=self.BackupCreate)
        self.BTN_createBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_createBackup = ttk.Button(self.FRAME_backupButtons, text="Create Named Backup", bootstyle="primary", 
                                   command=lambda: self.BackupCreate(isNamed=True))
        self.BTN_createBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.BTN_applyBackup = ttk.Button(self.FRAME_backupButtons, text="Apply Backup", bootstyle="danger", command=self.BackupApply)
        self.BTN_applyBackup.pack(side=LEFT, expand=True, padx=5, pady=5)
        self.PROG_backupProgress.pack(fill=X, padx=5, pady=5)

        self.FRAME_backupButtons.pack(fill=X, pady=5)
    
    def __setupGUI_FrameLeft(self):
        # Left panel for game list
        self.FRAME_left = ttk.Frame(self.FRAME_main)
        self.FRAME_main.add(self.FRAME_left, weight=1)

                # Treeview for the game list
        self.LIST_games = ttk.Treeview(self.FRAME_left, show='tree', selectmode='browse', bootstyle="info")
        self.LIST_games.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Grid for Treeview to expand
        self.LIST_games.bind("<<TreeviewSelect>>", self.onGameSelect)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.FRAME_left, orient=VERTICAL, command=self.LIST_games.yview, bootstyle="danger")
        scrollbar.grid(row=0, column=1, sticky="ns")  # Place scrollbar in the same row as Treeview, stretching vertically

        # Configure grid to make the Treeview expand properly
        self.FRAME_left.grid_rowconfigure(0, weight=1)  # Row 0 (Treeview) expands to fill the space
        self.FRAME_left.grid_columnconfigure(0, weight=1)  # Column 0 (Treeview) expands to fill the space

        # Configure the Treeview to use the scrollbar
        self.LIST_games.configure(yscrollcommand=scrollbar.set)

        # Add the "Add Missing Game" button at the bottom
        self.BTN_addMissingGame = ttk.Button(self.FRAME_left, text="Add Missing Game", bootstyle="info", command=self.__addMissingGame)
        self.BTN_addMissingGame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')  # Button at the bottom
        
            
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    SaveFileManager(root)
    root.mainloop()
