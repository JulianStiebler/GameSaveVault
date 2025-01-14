from dataclasses import dataclass, asdict
from typing import Dict, Optional

@dataclass
class GameResources:
    manual: Optional[str] = None
    guide: Optional[str] = None

@dataclass
class KnownGamePath:
    path_save: str
    image_header: Optional[str] = None
    resources: Optional[GameResources] = None

@dataclass
class InstalledGame:
    platform: str = "General"
    path_install: Optional[str] = None
    path_save: Optional[str] = None
    appid: Optional[str] = None
    name: Optional[str] = None
    installdir: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'InstalledGame':
        return cls(**{
            k: v for k, v in data.items() 
            if k in InstalledGame.__annotations__
        })

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}