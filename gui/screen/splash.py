"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style("darkly")  # Set ttkbootstrap style

        # Window size
        width = 400
        height = 200

        # Get screen dimensions
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()

        # Calculate position
        x = int((screenWidth / 2) - (width / 2))
        y = int((screenHeight / 2) - (height / 2))

        # Set window geometry
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.overrideredirect(True)

        # Get theme background color
        bgColor = self.style.colors.get("frame")  # Retrieve the frame background color
        self.root.configure(bg=bgColor)

        # Create the frame and apply the background color to match
        self.FRAME_mainSplash = ttk.Frame(self.root, bootstyle="primary")  # Set bootstyle
        self.FRAME_mainSplash.configure(style="TFrame")  # Explicitly match the ttkbootstrap theme
        self.FRAME_mainSplash.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Label for the progress text
        self.LBL_LoadupProgress = ttk.Label(
            self.FRAME_mainSplash,
            text="Initializing...",
            font=("Arial", 14),
            bootstyle="light"
        )
        self.LBL_LoadupProgress.pack(pady=20)

        # Progress bar
        self.PRG_Loadup = ttk.Progressbar(
            self.FRAME_mainSplash,
            mode='determinate',
            bootstyle="success"
        )
        self.PRG_Loadup.pack(fill=X, pady=10)

    def progressUpdate(self, value, text=None):
        self.PRG_Loadup['value'] = value
        if text:
            self.LBL_LoadupProgress.config(text=text)
        self.root.update_idletasks()

    def close(self):
        self.root.destroy()
