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
