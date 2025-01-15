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
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTTOM, LEFT, RIGHT, X

from core.enums import AppConfigGithub, AppConfig


class Footer:
    def __init__(self, root, data, app):
        self.root = root
        self.data = data
        self.app = app
        
        self.FRAME_footer = ttk.Frame(self.root)
        self.FRAME_footer.pack(side=BOTTOM, fill=X)
        
        links = {
            "GitHub": AppConfigGithub.GITHUB_URL_ORIGIN.value,
            "Feature Request": AppConfigGithub.GITHUB_URL_FEATUREREQUEST.value,
            "Bug Report": AppConfigGithub.GITHUB_URL_BUGREPORT.value
        }
        
        for name, url in links.items():
            self.LBL_FooterLink = ttk.Label(self.FRAME_footer, text=name, font=("Arial", 10), anchor="center", bootstyle="light")
            self.LBL_FooterLink.pack(side=LEFT, padx=10)
            self.LBL_FooterLink.bind("<Button-1>", lambda e, url=url: os.startfile(url))
            self.LBL_FooterLink.bind("<Enter>", lambda e, label=self.LBL_FooterLink: label.config(foreground="#1E90FF"))
            self.LBL_FooterLink.bind("<Leave>", lambda e, label=self.LBL_FooterLink: label.config(foreground="#FFFFFF"))
            
        # Create non-clickable version label on the bottom right
        LBL_Version = ttk.Label(self.FRAME_footer, text=AppConfig.VERSION.value, font=("Arial", 10), anchor="e", bootstyle="light")
        LBL_Version.pack(side=RIGHT, padx=10)