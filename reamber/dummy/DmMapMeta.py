from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


@dataclass
class DmMapMetaMetadata:
    title: str = ""
    artist: str = ""
    creator: str = ""
    version: str = ""


@dataclass
class DmMapMeta(DmMapMetaMetadata):
    """ The umbrella class that holds everything not included in HitObjects and TimingPoints """
    pass
