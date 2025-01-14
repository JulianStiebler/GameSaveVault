from dataclasses import dataclass, asdict
from typing import Dict, Optional
from pydantic import AnyUrl


@dataclass
class GameResources:
    manual: Optional[AnyUrl] = None
    guide: Optional[AnyUrl] = None
    wiki: Optional[AnyUrl] = None

@dataclass
class KnownGamePath:
    path_save: str
    image_header: Optional[AnyUrl] = None
    resources: Optional[GameResources] = None

@dataclass
class InstalledGame:
    name: str  # Required parameter
    path_install: Optional[str] = None
    path_save: Optional[str] = None
    appid: Optional[str] = None
    installdir: Optional[str] = None
    platform: str = "General"  # Default, but can be overridden
    
    @classmethod
    def from_dict(cls, name: str, data: dict) -> 'InstalledGame':
        # Keep existing platform if it's Steam or Epic, otherwise use General
        platform = data.get('platform', 'General')
        if platform not in ['Steam', 'Epic']:
            platform = 'General'
            
        return cls(
            name=name,
            platform=platform,
            path_install=data.get('path_install'),
            path_save=data.get('path_save'),
            appid=data.get('appid'),
            installdir=data.get('installdir')
        )

    def to_dict(self) -> dict:
        result = asdict(self)
        # Exclude name from output as it's the key in json
        return {k: v for k, v in result.items() 
                if v is not None and k != 'name'}