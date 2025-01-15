"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import ttkbootstrap as ttk

from core.app import SaveFileManager
from core import DataManager
from core.enums import AppConfig

from gui.screen.splash import SplashScreen

def initGameSaveVault(splash, steps, root, data):
    def step(index):
        if index < len(steps):
            text, func = steps[index]
            splash.progressUpdate((index + 1) * (100 // len(steps)), text)
            try:
                func()
            except Exception as e:
                print(f"Error during initialization: {e}")
            root.after(1000, step, index + 1)
        else:
            splash.close()
            root.deiconify()
            SaveFileManager(root, data)

    step(0)


if __name__ == "__main__":
    # Create main window first but don't show it
    dataObj = DataManager()
    ROOT_main = ttk.Window(themename=AppConfig.WINDOW_THEME.value)
    ROOT_main.withdraw()

    # Create and show splash screen as a Toplevel window
    ROOT_splash = ttk.Toplevel(ROOT_main)
    splashObj = SplashScreen(ROOT_splash)

    steps = [
        ("Initializing Epic Library...", dataObj.detectSystem.initEpicLibrary),
        ("Initializing Steam Library...", dataObj.detectSystem.initSteamLibrary),
        ("Initializing General Library...", dataObj.detectSystem.initGeneralLibrary),
        ("Loading Application Data...", dataObj.initApplication)
    ]

    initGameSaveVault(splashObj, steps, ROOT_main, dataObj)

    ROOT_splash.mainloop()
