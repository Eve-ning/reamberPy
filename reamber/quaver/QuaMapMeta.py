from dataclasses import dataclass, field
from typing import List, Dict


class QuaMapMode:
    """Lists all available Quaver Key modes.

    Though easy to implement the rest of the keys here
    """

    KEYS_4: str = "Keys4"
    KEYS_7: str = "Keys7"
    KEYS_8: str = "Keys8"  # Not officially supported yet.

    @staticmethod
    def get_keys(s: str) -> int:
        """Gets the keys as integer instead of string"""
        if s == QuaMapMode.KEYS_4:
            return 4
        elif s == QuaMapMode.KEYS_7:
            return 7
        elif s == QuaMapMode.KEYS_8:
            return 8
        else:
            return -1

    @staticmethod
    def get_mode(i: int) -> str:
        """Gets the keys as string instead of int"""
        if i == 4:
            return QuaMapMode.KEYS_4
        elif i == 7:
            return QuaMapMode.KEYS_7
        elif i == 8:
            return QuaMapMode.KEYS_8
        else:
            return ""


@dataclass
class QuaMapMeta:
    audio_file: str = ""
    song_preview_time: int = 0
    background_file: str = ""
    banner_file: str = ""
    genre: str = ""
    bpm_does_not_affect_scroll_velocity: bool = True
    initial_scroll_velocity: float = ""
    has_scratch_key: bool = True
    map_id: int = -1
    map_set_id: int = -1
    mode: str = QuaMapMode.KEYS_4
    title: str = ""
    artist: str = ""
    source: str = ""
    tags: List[str] = field(default_factory=lambda: [])
    creator: str = ""
    difficulty_name: str = ""
    description: str = ""
    editor_layers: List[str] = field(default_factory=lambda: [])
    custom_audio_samples: List[str] = field(default_factory=lambda: [])
    sound_effects: List[str] = field(default_factory=lambda: [])

    def _read_metadata(self, d: Dict):
        """Reads the Metadata dict from the YAML read"""
        self.audio_file = d.get('AudioFile', self.audio_file)
        self.song_preview_time = d.get('SongPreviewTime',
                                       self.song_preview_time)
        self.background_file = d.get('BackgroundFile', self.background_file)
        self.banner_file = d.get('BannerFile', self.banner_file)
        self.genre = d.get('Genre', self.genre)
        self.bpm_does_not_affect_scroll_velocity = d.get(
            'BPMDoesNotAffectScrollVelocity',
            self.bpm_does_not_affect_scroll_velocity)
        self.initial_scroll_velocity = d.get('InitialScrollVelocity',
                                             self.initial_scroll_velocity)
        self.has_scratch_key = d.get('HasScratchKey', self.has_scratch_key)
        self.map_id = d.get('MapId', self.map_id)
        self.map_set_id = d.get('MapSetId', self.map_set_id)
        self.mode = d.get('Mode', self.mode)
        self.title = d.get('Title', self.title)
        self.artist = d.get('Artist', self.artist)
        self.source = d.get('Source', self.source)
        # Tags are sep by " "
        self.tags = [i for i in d.get('Tags', "").split(" ") if i]
        self.creator = d.get('Creator', self.creator)
        self.difficulty_name = d.get('DifficultyName', self.difficulty_name)
        self.description = d.get('Description', self.description)
        self.editor_layers = d.get('EditorLayers', self.editor_layers)
        self.custom_audio_samples = d.get('CustomAudioSamples',
                                          self.custom_audio_samples)
        self.sound_effects = d.get('SoundEffects', self.sound_effects)

    def _write_meta(self) -> Dict:
        """Writes the metadata as a Dictionary and returns it"""
        return {
            'AudioFile': self.audio_file,
            'SongPreviewTime': self.song_preview_time,
            'BackgroundFile': self.background_file,
            'BannerFile': self.banner_file,
            'Genre': self.genre,
            'BPMDoesNotAffectScrollVelocity':
                self.bpm_does_not_affect_scroll_velocity,
            'InitialScrollVelocity': self.initial_scroll_velocity,
            'HasScratchKey': self.has_scratch_key,
            'MapId': self.map_id,
            'MapSetId': self.map_set_id,
            'Mode': self.mode,
            'Title': self.title,
            'Artist': self.artist,
            'Source': self.source,
            'Tags': " ".join(self.tags),
            'Creator': self.creator,
            'DifficultyName': self.difficulty_name,
            'Description': self.description,
            'EditorLayers': self.editor_layers,
            'CustomAudioSamples': self.custom_audio_samples,
            'SoundEffects': self.sound_effects,
        }
