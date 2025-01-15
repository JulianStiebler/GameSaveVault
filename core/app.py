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

        self.ELEM_details.updateDetailsView()
        self.ELEM_details.updateLIST_fileExplorer()
        self.ELEM_details.updateLIST_backupContents()
        
            
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    GameSaveVault(root)
    root.mainloop()
