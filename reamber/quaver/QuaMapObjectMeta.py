from dataclasses import dataclass, field
from typing import List, Dict


class QuaMapObjectMode:
    KEYS_4: str = "Keys4"
    KEYS_7: str = "Keys7"

    @staticmethod
    def keys(s: str) -> int:
        """ Gets the keys as integer instead of string """
        if   s == QuaMapObjectMode.KEYS_4: return 4
        elif s == QuaMapObjectMode.KEYS_7: return 7
        else: return -1

    @staticmethod
    def str(i: int) -> str:
        """ Gets the keys as string instead of int """
        if   i == 4: return QuaMapObjectMode.KEYS_4
        elif i == 7: return QuaMapObjectMode.KEYS_7
        else: return ""


@dataclass
class QuaMapObjectMeta:
    audioFile: str                  = ""
    songPreviewTime: int            = 0
    backgroundFile: str             = ""
    mapId: int                      = -1
    mapSetId: int                   = -1
    mode: str                       = QuaMapObjectMode.KEYS_4
    title: str                      = ""
    artist: str                     = ""
    source: str                     = ""
    tags: str                       = ""  # Stated as '', should it be []? List[str]?
    creator: str                    = ""
    difficultyName: str             = ""
    description: str                = ""
    editorLayers: List[str]         = field(default_factory=lambda: [])
    customAudioSamples: List[str]   = field(default_factory=lambda: [])
    soundEffects: List[str]         = field(default_factory=lambda: [])

    def _readMetadata(self, d: Dict):
        """ Reads the Metadata Dictionary provided by the YAML Library
        :param d: This is simply the whole Dictionary after the TPs and Notes are popped
        """
        self.audioFile          = d['AudioFile']
        self.songPreviewTime    = d['SongPreviewTime']
        self.backgroundFile     = d['BackgroundFile']
        self.mapId              = d['MapId']
        self.mapSetId           = d['MapSetId']
        self.mode               = d['Mode']
        self.title              = d['Title']
        self.artist             = d['Artist']
        self.source             = d['Source']
        self.tags               = d['Tags']
        self.creator            = d['Creator']
        self.difficultyName     = d['DifficultyName']
        self.description        = d['Description']
        self.editorLayers       = d['EditorLayers']
        self.customAudioSamples = d['CustomAudioSamples']
        self.soundEffects       = d['SoundEffects']

    def _writeMeta(self) -> Dict:
        """ Writes the metadata as a Dictionary and returns it """
        return {
            'AudioFile': self.audioFile,
            'SongPreviewTime': self.songPreviewTime,
            'BackgroundFile': self.backgroundFile,
            'MapId': self.mapId,
            'MapSetId': self.mapSetId,
            'Mode': self.mode,
            'Title': self.title,
            'Artist': self.artist,
            'Source': self.source,
            'Tags': self.tags,
            'Creator': self.creator,
            'DifficultyName': self.difficultyName,
            'Description': self.description,
            'EditorLayers': self.editorLayers,
            'CustomAudioSamples': self.customAudioSamples,
            'SoundEffects': self.soundEffects
        }
