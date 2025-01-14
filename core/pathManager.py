import os
from typing import Dict, Optional

class PathManager:
    """Handles path conversion between absolute and relative paths"""
    
    def __init__(self):
        # Cache system paths in normalized form
        self.SYSTEM_PATHS = {
            '%localappdata%': os.path.normpath(os.environ.get('LOCALAPPDATA', '')),
            '%appdata%': os.path.normpath(os.environ.get('APPDATA', '')),
            '%programfiles%': os.path.normpath(os.environ.get('PROGRAMFILES', '')),
            '%programfiles(x86)%': os.path.normpath(os.environ.get('PROGRAMFILES(X86)', '')),
            '%userprofile%': os.path.normpath(os.environ.get('USERPROFILE', '')),
        }
        
        # Cache username for user folder detection
        self.USERNAME = os.environ.get('USERNAME', '')

    def path_make_relative(self, path: str) -> str:
        """Convert absolute path to relative using environment variables"""
        if not path:
            return path
            
        normalizedPath = os.path.normpath(path).lower()
        
        # Sort by specificity - try most specific paths first
        sortedPath = sorted(
            self.SYSTEM_PATHS.items(),
            key=lambda x: (
                # Primary sort by path specificity (more segments = more specific)
                len(x[1].split(os.sep)),
                # Secondary sort by path length
                len(x[1])
            ),
            reverse=True  # Most specific first
        )
        
        for envVar, sysPath in sortedPath:
            if normalizedPath.startswith(sysPath.lower()):
                return path.replace(sysPath, envVar)
                
        return path

    @staticmethod
    def path_check_relative(path: str) -> bool:
        return any(var.lower() in path.lower() for var in ['%userprofile%', '%appdata%', 
                                                          '%localappdata%', '%programfiles%'])

    @staticmethod
    def path_expand(path: str, gamePathInstall: Optional[str] = None) -> str:
        if gamePathInstall and '%gameinstall%' in path:
            path = path.replace('%gameinstall%', gamePathInstall)
        return os.path.normpath(os.path.expandvars(path))