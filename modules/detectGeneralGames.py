"""
# Github Authors: https://github.com/JulianStiebler/
# Github Contributors: https://github.com/JulianStiebler/

# GitHub Repository: https://github.com/JulianStiebler/GameSaveVault 
# Github License: MIT // https://github.com/JulianStiebler/GameSaveVault/blob/main/LICENSE

# Last Edited: 11.01.2025
"""

import os
import json
from pathlib import Path

class DetectGamesGeneral:
    def __init__(self):
        pass
        
    @staticmethod
    def GetSaveFolders(knownGamePaths, outputFile):
        def helper_expandPath(path: str, installedGames: dict, game: str) -> str:
            """Helper function to expand path and resolve '%gameinstall%'."""
            # Check if the path contains '%gameinstall%' and resolve it
            if "%gameinstall%" in path:
                # Ensure the game exists in installedGames
                if game in installedGames and 'install_path' in installedGames[game]:
                    # Replace '%gameinstall%' with the install_path
                    install_path = installedGames[game]['install_path']
                    path = path.replace("%gameinstall%", install_path)
                else:
                    print(f"Install path for '{game}' not found in installedGames.json.")
                    return None
            # Normalize and expand the path
            expandedPath = os.path.expandvars(path)
            return os.path.normpath(expandedPath)

        # Read the input JSON file containing save paths
        try:
            with open(knownGamePaths, 'r') as f:
                inputData = json.load(f)
        except FileNotFoundError:
            print(f"Input JSON file '{knownGamePaths}' not found.")
            return
        
        try:
            with open(outputFile, 'r') as f:
                installedGames = json.load(f)
        except FileNotFoundError:
            print(f"Installed games file '{outputFile}' not found.")
            return
        except Exception as e:
            print(f"Error reading '{outputFile}': {e}")
            return
        
        # Iterate through the game paths in the input JSON and check if they exist
        for game, path in inputData.get("Savepaths", {}).items():
            # Get the expanded save path
            expandedPath = helper_expandPath(path, installedGames, game)

            if expandedPath is None:
                continue

            # Debugging: print the expanded path to check if it's correct
            print(f"Checking save path for '{game}': {expandedPath}")

            # Ensure path ends with a backslash
            if not expandedPath.endswith(os.sep):
                expandedPath = expandedPath + os.sep

            # Check if the path exists
            if Path(expandedPath).exists():
                print(f"Found valid save path for '{game}': {expandedPath}")
                
                # Add or update the save path for the game in installedGames
                if game in installedGames:
                    installedGames[game]['save_path'] = expandedPath  # Update save_path
                else:
                    # If the game does not exist, create a new entry with save_path only
                    installedGames[game] = {"save_path": expandedPath}
                    
                if 'platform' not in installedGames[game] or not installedGames[game]['platform']:
                    installedGames[game]['platform'] = "General"  # Update platform only if not already set
            else:
                print(f"Save path does not exist for '{game}': {expandedPath}")

        # Write the updated installedGames data back to the file
        try:
            with open(outputFile, 'w') as f:
                json.dump(installedGames, f, indent=4)
            print(f"Games saved to {outputFile}")
        except Exception as e:
            print(f"Error writing to '{outputFile}': {e}")
