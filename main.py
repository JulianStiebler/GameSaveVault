"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

from core.app import SaveFileManager
from gui.screen.splash import SplashScreen
from core.dataManager import DataManager
import ttkbootstrap as ttk

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
    data = DataManager()
    ROOT_main = ttk.Window(themename=data.WINDOW_STYLE)
    ROOT_main.withdraw()

    # Create and show splash screen as a Toplevel window
    ROOT_splash = ttk.Toplevel(ROOT_main)
    splash = SplashScreen(ROOT_splash)

    steps = [
        ("Initializing Epic Library...", data.initEpicLibrary),
        ("Initializing Steam Library...", data.initSteamLibrary),
        ("Initializing General Library...", data.initGeneralLibrary),
        ("Loading Application Data...", data.initApplication)
    ]

    initGameSaveVault(splash, steps, ROOT_main, data)

    ROOT_splash.mainloop()
