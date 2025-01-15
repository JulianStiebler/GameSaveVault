"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import os
import re
from core.enums import AppStates, AppConfig

invalidChars = r'[\/:*?"<>|]'
class Utility:
    def __init__(self):
        pass
    
    @staticmethod
    def adjustTreeviewHeight(treeview, maxItems=10):
            """Adjust the height of a Treeview dynamically."""
            itemsCount = len(treeview.get_children())
            treeview["height"] = min(itemsCount, maxItems)
    
        
    @staticmethod
    def sanitizeFolderName_fix(name):
        """Replace invalid characters for folder names with an underscore."""
        return re.sub(invalidChars, '_', name)

    @staticmethod
    def sanitizeFolderName_contains(name):
            # List of invalid characters in windows filenames
            return bool(re.search(invalidChars, name))
        
    @staticmethod
    def openFolderInExplorer(path):
        os.startfile(path)
        
    @staticmethod
    def debugPrint(message):
        if AppConfig.STATE == AppStates.DEBUG:
            print(message)