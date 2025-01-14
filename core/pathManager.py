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

    def make_relative(self, path: str) -> str:
        """Convert absolute path to relative using environment variables"""
        if not path:
            return path
            
        norm_path = os.path.normpath(path).lower()
        
        # Sort by specificity - try most specific paths first
        sorted_paths = sorted(
            self.SYSTEM_PATHS.items(),
            key=lambda x: (
                # Primary sort by path specificity (more segments = more specific)
                len(x[1].split(os.sep)),
                # Secondary sort by path length
                len(x[1])
            ),
            reverse=True  # Most specific first
        )
        
        for env_var, sys_path in sorted_paths:
            if norm_path.startswith(sys_path.lower()):
                return path.replace(sys_path, env_var)
                
        return path

    @staticmethod
    def is_relative_path(path: str) -> bool:
        return any(var.lower() in path.lower() for var in ['%userprofile%', '%appdata%', 
                                                          '%localappdata%', '%programfiles%'])

    @staticmethod
    def expand_path(path: str, game_path_install: Optional[str] = None) -> str:
        if game_path_install and '%gameinstall%' in path:
            path = path.replace('%gameinstall%', game_path_install)
        return os.path.normpath(os.path.expandvars(path))