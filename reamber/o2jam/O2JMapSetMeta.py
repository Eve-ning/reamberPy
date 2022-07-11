"""This holds the metadata for the O2Jam Map Set

Directly inherited by O2JMapSet to allow access to all the extra metadata
"""

import struct
from dataclasses import dataclass, field
from typing import List


class O2JMapGenre:
    """This is a class of static variables that indicate the genre of the song"""
    BALLAD: int = 0
    ROCK: int = 1
    DANCE: int = 2
    TECHNO: int = 3
    HIP_HOP: int = 4
    SOUL_R_B: int = 5
    JAZZ: int = 6
    FUNK: int = 7
    CLASSICAL: int = 8
    TRADITIONAL: int = 9
    ETC: int = 10


@dataclass
class O2JMapSetMeta:
    """This class contains the readable metadata of the map

    This can be extracted from the first 300 bytes of every ojn file."""

    #                                                             # FORMAT
    song_id: int = 0  # INT
    signature: str = ""  # CHAR[4]
    encode_version: float = 0.0  # FLOAT
    genre: int = 0  # INT
    bpm: float = 0.0  # FLOAT
    level: List[int] = field(default_factory=list)  # SHORT[4]
    event_count: List[int] = field(default_factory=list)  # INT[3]
    note_count: List[int] = field(default_factory=list)  # INT[3]
    measure_count: List[int] = field(default_factory=list)  # INT[3]
    package_count: List[int] = field(default_factory=list)  # INT[3]
    old_encode_version: int = 0  # SHORT
    old_song_id: int = 0  # SHORT
    old_genre: bytes = b""  # CHAR[20]
    bmp_size: int = 0  # INT
    old_file_version: int = 0  # INT
    title: str = ""  # CHAR[64]
    artist: str = ""  # CHAR[32]
    creator: str = ""  # CHAR[32]
    ojm_file: str = ""  # CHAR[32]
    cover_size: int = 0  # INT
    duration: List[int] = field(default_factory=list)  # INT[3]
    note_offset: List[int] = field(default_factory=list)  # INT[3]
    cover_offset: int = 0  # INT

    BYTE_COUNT = [1, 4, 1, 1, 1, 4, 3, 3, 3, 3, 1, 1, 20, 1, 1, 64, 32, 32, 32,
                  1, 3, 3, 1]
    BYTE_SIZES = [4, 4, 4, 4, 4, 8, 12, 12, 12, 12, 2, 2, 20, 4, 4, 64, 32, 32,
                  32, 4, 12, 12, 4]
    BYTE_FORMATS = ["i", "s", "f", "i", "f", "h", "i", "i", "i", "i", "h", "h",
                    "s", "i", "i", "s", "s", "s", "s", "i", "i", "i", "i"]

    def read_meta(self, metadata: bytes):
        """Reads the metadata of the map

        Args:
            metadata: The first 300 bytes go here
        """
        meta_fields: List = []
        ix_start = 0
        for fmt, size, count in zip(O2JMapSetMeta.BYTE_FORMATS,
                                    O2JMapSetMeta.BYTE_SIZES,
                                    O2JMapSetMeta.BYTE_COUNT):
            meta_field = []
            fmt_size = int(size / count)
            for _ in range(count):
                meta_field.append(
                    struct.unpack("<" + fmt,
                                  metadata[ix_start:ix_start + fmt_size])[0]
                )
                ix_start += fmt_size
            meta_fields.append(meta_field)

        def decode_replace(b: bytes):
            return (b"".join(filter(lambda x: x != b'\x00', b))
                    .decode("ascii", errors='ignore'))

        self.song_id = meta_fields[0][0]
        self.signature = decode_replace(meta_fields[1])
        self.encode_version = meta_fields[2][0]
        self.genre = meta_fields[3][0]
        self.bpm = meta_fields[4][0]
        self.level = meta_fields[5]
        self.event_count = meta_fields[6]
        self.note_count = meta_fields[7]
        self.measure_count = meta_fields[8]
        self.package_count = meta_fields[9]
        self.old_encode_version = meta_fields[10][0]
        self.old_song_id = meta_fields[11][0]
        self.old_genre = b"".join(meta_fields[12])
        self.bmp_size = meta_fields[13][0]
        self.old_file_version = meta_fields[14][0]
        self.title = decode_replace(meta_fields[15])
        self.artist = decode_replace(meta_fields[16])
        self.creator = decode_replace(meta_fields[17])
        self.ojm_file = decode_replace(meta_fields[18])
        self.cover_size = meta_fields[19][0]
        self.duration = meta_fields[20]
        self.note_offset = meta_fields[21]
        self.cover_offset = meta_fields[22][0]

    def write_meta(self, f) -> bytes:
        """Unimplemented, writes the metadata of a ojn file

        I don't think I'll implement this unless there's clear support on this
        """
        pass
        # need to verify all byte sizes on export
        # f.write(struct.pack("<i", self.songId                            ))
        # f.write(bytes(self.signature, encoding='ascii'                   ))
        # f.write(struct.pack("<f", self.encodeVersion                     ))
        # f.write(struct.pack("<i", self.genre                             ))
        # f.write(struct.pack("<f", self.bpm                               ))
        # for level in self.level:
        #     f.write(struct.pack("<h", level                              ))
        # for eventCount in self.eventCount:
        #     f.write(struct.pack("<i", eventCount                         ))
        # for noteCount in self.noteCount:
        #     f.write(struct.pack("<i", noteCount                          ))
        # for measureCount in self.measureCount:
        #     f.write(struct.pack("<i", measureCount                       ))
        # for packageCount in self.packageCount:
        #     f.write(struct.pack("<i", packageCount                       ))
        # f.write(struct.pack("<h", self.oldEncodeVersion                  ))
        # f.write(struct.pack("<h", self.oldSongId                         ))
        # f.write(self.oldGenre                                             )
        # f.write(struct.pack("<i", self.bmpSize                           ))
        # f.write(struct.pack("<i", self.oldFileVersion                    ))
        # # TO#DO: Need to verify length. Fly Magpie is 63, expect 64 bytes
        # f.write(bytes(self.title, encoding='ascii')                       )
        # f.write(struct.pack("<s", bytes(self.artist, encoding='ascii')   ))
        # f.write(struct.pack("<s", bytes(self.creator, encoding='ascii')  ))
        # f.write(struct.pack("<s", bytes(self.ojmFile, encoding='ascii')  ))
        # f.write(struct.pack("<i", self.coverSize                         ))
        # for duration in self.duration:
        #     f.write(struct.pack("<i", self.duration                      ))
        # for noteOffset in self.noteOffset:
        #     f.write(struct.pack("<i", noteOffset                         ))
        # f.write(struct.pack("<i", self.coverOffset                       ))
