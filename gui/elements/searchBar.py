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

class SearchBar:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        
        
        INP_SearchBar = ttk.Entry(self.app.FRAME_top, textvariable=self.app.searchVar, font=("Arial", 14))
        INP_SearchBar.pack(fill=X, padx=10, pady=5)