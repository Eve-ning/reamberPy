from dataclasses import dataclass


@dataclass
class SMMapObjectMeta:
    title: str = ""
    subtitle: str = ""
    artist: str = ""
    titleTranslit: str = ""
    subtitleTranslit: str = ""
    artistTranslit: str = ""
    genre: str = ""
    credit: str = ""
    banner: str = ""
    background: str = ""
    lyricsPath: str = ""
    cdTitle: str = ""
    music: str = ""
    offset: float = 0.0
    # BPMS
    # STOPS
    sampleStart: float = 0.0
    sampleLength: float = 0.0
    displayBpm: str = ""
    selectable: bool = True
    bgChanges: str = ""  # Idk what this does
    fgChanges: str = ""  # Idk what this does


