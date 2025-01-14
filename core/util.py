"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import os
import zipfile
import re

invalidChars = r'[\/:*?"<>|]'

@staticmethod
def openFolderInExplorer(path):
    os.startfile(path)

@staticmethod
def zipFolder(sourceFolder, zipFilePath, progressCallback=None):
    # Count total files first
    total_files = sum([len(files) for _, _, files in os.walk(sourceFolder)])
    current_file = 0
    
    with zipfile.ZipFile(zipFilePath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(sourceFolder):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, sourceFolder)
                zipf.write(filepath, arcname)
                current_file += 1
                if progressCallback:
                    progress = (current_file / total_files) * 100
                    progressCallback(progress)

@staticmethod
def extractZIPContent(zipFilePath, targetFolder):
    with zipfile.ZipFile(zipFilePath, 'r') as zipf:
        os.makedirs(targetFolder, exist_ok=True)
        zipf.extractall(targetFolder)

@staticmethod
def sanitizeFolderName_fix(name):
    """Replace invalid characters for folder names with an underscore."""
    return re.sub(invalidChars, '_', name)

@staticmethod
def sanitizeFolderName_contains(name):
        # List of invalid characters in windows filenames
        return bool(re.search(invalidChars, name))

@staticmethod
def adjustTreeviewHeight(treeview, maxItems=10):
        """Adjust the height of a Treeview dynamically."""
        itemsCount = len(treeview.get_children())
        treeview["height"] = min(itemsCount, maxItems)
        