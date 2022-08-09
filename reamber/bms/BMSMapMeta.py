from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class BMSMapMetaMetadata:
    title: bytes = b""
    artist: bytes = b""
    version: bytes = b""
    samples: dict = field(default_factory=lambda: {})
    misc: dict = field(default_factory=lambda: {})


@dataclass
class BMSMapMetaMisc:
    ln_end_channel: bytes = b'ZZ'
    exbpms: Dict[bytes, float] = field(default_factory=lambda: {})


@dataclass
class BMSMapMeta(BMSMapMetaMetadata, BMSMapMetaMisc):
    """Holds all metadata/header info"""
    pass

# class BMSMapMode:
#     """Determines the map type from #PLAYER X.
#
#     Currently not too sure if this is reliable.
#     If possible, use bms.notes.maxColumn() + 1 to grab keys.
#
#     This is also agreed upon by other engines:
#
#     - LR2, nanasi, ruvit, and pomu2 disregard #PLAYER and
#     guess actual play mode by the parsed channels.
#     """
#
#     SINGLE = 1
#     COUPLE = 2
#     DOUBLE = 3
#     BATTLE = 4
