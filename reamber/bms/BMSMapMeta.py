from __future__ import annotations
from typing import List
from dataclasses import dataclass, field


class BMSMapMode:
    SINGLE = 1
    COUPLE = 2
    DOUBLE = 3
    BATTLE = 4


@dataclass
class BMSMapMetaMetadata:
    mode: int = BMSMapMode.SINGLE
    title: str = ""
    artist: str = ""
    version: str = ""
    misc: dict = field(default_factory=lambda: {})



@dataclass
class BMSMapMeta(BMSMapMetaMetadata):
    """ The umbrella class that holds everything not included in HitObjects and TimingPoints """
    pass

    def readHeader(self, header: List[bytes]):
        pass