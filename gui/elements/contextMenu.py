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

class ContextMenu:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        self.menu_bar = ttk.Menu(self.root)
        self._setup_menu()
        self.root.config(menu=self.menu_bar)

    def _setup_menu(self):
        # Program menu
        program_menu = ttk.Menu(self.menu_bar, tearoff=0)
        program_menu.add_command(label="Exit", command=self.root.quit)  # Placeholder Exit command
        program_menu.add_command(label="Reload Epic Library", command=self.data.detectSystem.initEpicLibrary)
        self.menu_bar.add_cascade(label="Program", menu=program_menu)
        
        # Add more menus if needed
        # Example: Help menu
        help_menu = ttk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def _show_about(self):
        # Placeholder for About functionality
        ttk.messagebox.showinfo("About", "This is a sample application.")
