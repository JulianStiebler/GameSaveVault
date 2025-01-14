"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import tkinter as tk  # Import tkinter as tk
from tkinter import filedialog, messagebox  # Additional components needed for dialogs
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os

class AddMissingGameDialog:
    def __init__(self, root, data_manager=None):
        self.result = None
        self.data = data_manager
        self.dialog = ttk.Toplevel(root)
        self.dialog.title("Add Missing Game")
        self.dialog.geometry("500x350")
        self.dialog.resizable(False, False)
        self.dialog.transient(root)
        self.dialog.grab_set()

        # Main frame
        self.FRAME_main = ttk.Frame(self.dialog, padding=20)
        self.FRAME_main.pack(fill=BOTH, expand=True)

        # Game name
        self.LBL_name = ttk.Label(self.FRAME_main, text="Game Name:", font=("Arial", 12))
        self.LBL_name.pack(anchor=W, pady=(0, 5))
        
        self.name = ttk.StringVar()
        self.INP_name = ttk.Entry(self.FRAME_main, textvariable=self.name, font=("Arial", 12))
        self.INP_name.pack(fill=X, pady=(0, 10))

        # Save path
        self.LBL_savePath = ttk.Label(self.FRAME_main, text="Save Path:", font=("Arial", 12))
        self.LBL_savePath.pack(anchor=W, pady=(0, 5))
        
        self.FRAME_savePath = ttk.Frame(self.FRAME_main)
        self.FRAME_savePath.pack(fill=X, pady=(0, 10))
        
        self.savePath = ttk.StringVar()
        self.INP_savePath = ttk.Entry(self.FRAME_savePath, textvariable=self.savePath, font=("Arial", 12))
        self.INP_savePath.pack(side=LEFT, fill=X, expand=True)
        
        self.BTN_browseSave = ttk.Button(self.FRAME_savePath,  text="Browse",  command=self.__browseSavePath, bootstyle="secondary")
        self.BTN_browseSave.pack(side=RIGHT, padx=(5, 0))

        # Install path
        self.LBL_installPath = ttk.Label(self.FRAME_main, text="Install Path:", font=("Arial", 12))
        self.LBL_installPath.pack(anchor=W, pady=(0, 5))
        
        self.FRAME_installPath = ttk.Frame(self.FRAME_main)
        self.FRAME_installPath.pack(fill=X, pady=(0, 10))
        
        self.installPath = ttk.StringVar()
        self.INP_installPath = ttk.Entry(self.FRAME_installPath, textvariable=self.installPath, font=("Arial", 12))
        self.INP_installPath.pack(side=LEFT, fill=X, expand=True)
        
        self.BTN_browseInstall = ttk.Button(self.FRAME_installPath, text="Browse", command=self.__browseInstallPath,bootstyle="secondary")
        self.BTN_browseInstall.pack(side=RIGHT, padx=(5, 0))

        # Is installed checkbox
        self.isInstalled = ttk.BooleanVar(value=False)
        self.CHK_isInstalled = ttk.Checkbutton(self.FRAME_main,text="Is Installed?",variable=self.isInstalled,bootstyle="primary")
        self.CHK_isInstalled.pack(anchor=W, pady=(10, 15))

        # Buttons
        self.FRAME_buttons = ttk.Frame(self.dialog)
        self.FRAME_buttons.pack(fill=X, pady=10)
        
        self.BTN_add = ttk.Button(self.FRAME_buttons, text="Add", command=self.__buttonOkay, bootstyle="success")
        self.BTN_add.pack(side=RIGHT, padx=5)
        
        self.BTN_cancel = ttk.Button(self.FRAME_buttons, text="Cancel", command=self.__buttonCancel, bootstyle="danger")
        self.BTN_cancel.pack(side=RIGHT, padx=5)

        self.dialog.wait_window()

    def __browseSavePath(self):
        path = filedialog.askdirectory(title="Select Save Path")
        if path:
            self.savePath.set(path)

    def __browseInstallPath(self):
        path = filedialog.askdirectory(title="Select Install Path")
        if path:
            self.installPath.set(path)

    def __buttonOkay(self):
        name = self.name.get().strip()
        savePath = self.savePath.get().strip()
        installPath = self.installPath.get().strip()
        isInstalled = self.isInstalled.get()

        if not name:
            messagebox.showerror("Error", "Game name cannot be empty.", parent=self.dialog)
            return

        # Load current data
        customGames = self.data.loadJSON(self.data.PATH_customGames) if os.path.exists(self.data.PATH_customGames) else {"CustomPaths": {}}
        installedGames = self.data.loadJSON(self.data.pathInstalledGames) if os.path.exists(self.data.pathInstalledGames) else {}

        # Check if game exists in installed games
        if name in installedGames:
            messagebox.showerror("Error", f"The game '{name}' is already installed!", parent=self.dialog)
            return

        # Check if game exists in custom games but wants to be installed
        if name in customGames["CustomPaths"] and not isInstalled:
            messagebox.showerror("Error", f"The game '{name}' already exists in custom games!", parent=self.dialog)
            return

        # Allow adding to installed games even if in custom games
        self.result = {
            "name": name,
            "savePath": savePath if savePath else None,
            "installPath": installPath if installPath else None,
            "isInstalled": isInstalled
        }
        self.dialog.destroy()

    def __buttonCancel(self):
        self.result = None
        self.dialog.destroy()
