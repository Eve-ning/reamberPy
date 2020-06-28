""" This holds the metadata for the O2Jam Map Set

This is directly inherited by O2JMapSetObj to allow acsess to all the extra metadata
"""

from dataclasses import dataclass, field
from typing import List
import struct


class O2JMapGenre:
    """ This is a class of static variables that indicate the genre of the song """
    BALLAD     : int = 0
    ROCK       : int = 1
    DANCE      : int = 2
    TECHNO     : int = 3
    HIP_HOP    : int = 4
    SOUL_R_B   : int = 5
    JAZZ       : int = 6
    FUNK       : int = 7
    CLASSICAL  : int = 8
    TRADITIONAL: int = 9
    ETC        : int = 10


@dataclass
class O2JMapSetObjMeta:
    """ This class contains the readable metadata of the map

    This can be extracted from the first 300 bytes of every ojn file."""

    #                                                                # FORMAT   # LENGTH  # STARTS  # ENDS
    songId          : int       = 0                                  # INT      # 4       # 0       # 4
    signature       : str       = ""                                 # CHAR[4]  # 4       # 4       # 8
    encodeVersion   : float     = 0.0                                # FLOAT    # 4       # 8       # 12
    genre           : int       = 0                                  # INT      # 4       # 12      # 16
    bpm             : float     = 0.0                                # FLOAT    # 4       # 16      # 20
    level           : List[int] = field(default_factory=lambda: [])  # SHORT[4] # 8       # 20      # 28
    eventCount      : List[int] = field(default_factory=lambda: [])  # INT[3]   # 12      # 28      # 40
    noteCount       : List[int] = field(default_factory=lambda: [])  # INT[3]   # 12      # 40      # 52
    measureCount    : List[int] = field(default_factory=lambda: [])  # INT[3]   # 12      # 52      # 64
    packageCount    : List[int] = field(default_factory=lambda: [])  # INT[3]   # 12      # 64      # 76
    oldEncodeVersion: int       = 0                                  # SHORT    # 2       # 76      # 78
    oldSongId       : int       = 0                                  # SHORT    # 2       # 78      # 80
    oldGenre        : bytes     = b""                                # CHAR[20] # 20      # 80      # 100
    bmpSize         : int       = 0                                  # INT      # 4       # 100     # 104
    oldFileVersion  : int       = 0                                  # INT      # 4       # 104     # 108
    title           : str       = ""                                 # CHAR[64] # 64      # 108     # 172
    artist          : str       = ""                                 # CHAR[32] # 32      # 172     # 204
    creator         : str       = ""                                 # CHAR[32] # 32      # 204     # 236
    ojmFile         : str       = ""                                 # CHAR[32] # 32      # 236     # 268
    coverSize       : int       = 0                                  # INT      # 4       # 268     # 272
    duration        : List[int] = field(default_factory=lambda: [])  # INT[3]   # 12      # 272     # 284
    noteOffset      : List[int] = field(default_factory=lambda: [])  # INT[3]   # 12      # 284     # 296
    coverOffset     : int       = 0                                  # INT      # 4       # 296     # 300

    BIT_COUNT   = [1,   4,   1,   1,   1,   4,   3,   3,   3,   3,   1,   1,   20,  1,   1,   64,  32,  32,  32,
                   1,   3,   3,   1]
    BIT_SIZES   = [4,   4,   4,   4,   4,   8,   12,  12,  12,  12,  2,   2,   20,  4,   4,   64,  32,  32,  32,
                   4,   12,  12,  4]
    BIT_FORMATS = ["i", "s", "f", "i", "f", "h", "i", "i", "i", "i", "h", "h", "s", "i", "i", "s", "s", "s", "s",
                   "i", "i", "i", "i"]

    def readMeta(self, metadata: bytes):
        """ Reads the metadata of the map

        :param metadata: The first 300 bytes go here
        """
        metaFields: List = []
        indexStart = 0
        for fmt, size, count in zip(O2JMapSetObjMeta.BIT_FORMATS,
                                    O2JMapSetObjMeta.BIT_SIZES,
                                    O2JMapSetObjMeta.BIT_COUNT):
            metaField = []
            size_ = int(size / count)
            for i in range(count):
                metaField.append(struct.unpack("<" + fmt, metadata[indexStart:indexStart + size_])[0])
                indexStart += size_
            metaFields.append(metaField)
        self.songId           = metaFields[0][0]
        self.signature        = b"".join(metaFields[1]).decode("ascii", errors='ignore').replace('\x00', '')
        self.encodeVersion    = metaFields[2][0]
        self.genre            = metaFields[3][0]
        self.bpm              = metaFields[4][0]
        self.level            = metaFields[5]
        self.eventCount       = metaFields[6]
        self.noteCount        = metaFields[7]
        self.measureCount     = metaFields[8]
        self.packageCount     = metaFields[9]
        self.oldEncodeVersion = metaFields[10][0]
        self.oldSongId        = metaFields[11][0]
        self.oldGenre         = b"".join(metaFields[12])
        self.bmpSize          = metaFields[13][0]
        self.oldFileVersion   = metaFields[14][0]
        self.title            = b"".join(metaFields[15]).decode("ascii", errors='ignore').replace('\x00', '')
        self.artist           = b"".join(metaFields[16]).decode("ascii", errors='ignore').replace('\x00', '')
        self.creator          = b"".join(metaFields[17]).decode("ascii", errors='ignore').replace('\x00', '')
        self.ojmFile          = b"".join(metaFields[18]).decode("ascii", errors='ignore').replace('\x00', '')
        self.coverSize        = metaFields[19][0]
        self.duration         = metaFields[20]
        self.noteOffset       = metaFields[21]
        self.coverOffset      = metaFields[22][0]

    def writeMeta(self, f) -> bytes:
        """ Unimplemented, writes the metadata of a ojn file

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
