from dataclasses import dataclass, field
from typing import List, Dict

from reamber.base.Map import Map
from reamber.base.lists.TimedList import TimedList
from reamber.dummy.DmBpm import DmBpm
from reamber.dummy.DmHit import DmHit
from reamber.dummy.DmHold import DmHold
from reamber.dummy.DmMapMeta import DmMapMeta
from reamber.dummy.lists.DmBpmList import DmBpmList
from reamber.dummy.lists.DmNotePkg import DmNotePkg
from reamber.dummy.lists.DmSvList import DmSvList


@dataclass
class DmMap(Map, DmMapMeta):

    notes: DmNotePkg = field(default_factory=lambda: DmNotePkg())
    bpms:  DmBpmList = field(default_factory=lambda: DmBpmList())
    svs:   DmSvList  = field(default_factory=lambda: DmSvList())

    def init_hits(self,
                  note_cols: List[int],
                  note_offsets: List[float]):

        assert len(note_cols) == len(note_offsets), "Note Cols and Offset lengths must match."
        hits = self.notes.hits()
        [hits.append(DmHit(column=col, offset=offset)) for col, offset in zip(note_cols, note_offsets)]

    def init_holds(self,
                   note_cols: List[int],
                   note_offsets: List[float],
                   note_lengths: List[float]):

        assert len(note_cols) == len(note_offsets) == len(note_lengths), "Note Cols, offset, length lengths must match."
        holds = self.notes.holds()
        [holds.append(DmHold(column=col, offset=offset, _length=length))
         for col, offset, length in zip(note_cols, note_offsets, note_lengths)]

    def init_bpms(self,
                  bpms: List[float],
                  bpm_offsets: List[float]):

        assert len(bpms) == len(bpm_offsets), "Note Cols, offset, length lengths must match."
        [self.bpms.append(DmBpm(bpm=bpm, offset=offset)) for bpm, offset in zip(bpms, bpm_offsets)]

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms,
                'svs': self.svs}

    def scroll_speed(self, center_bpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType. Overrides the base to include SV
    
        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param center_bpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """
    
        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if center_bpm is None: center_bpm = 1
    
        sv_pairs = [(offset, multiplier) for offset, multiplier in zip(self.svs.sorted().offsets(),
                                                                       self.svs.multipliers())]
        bpm_pairs = [(offset, bpm) for offset, bpm in zip(self.bpms.offsets(), self.bpms.bpms())]
    
        curr_bpm_iter = 0
        next_bpm_offset = None if len(bpm_pairs) == 1 else bpm_pairs[1][0]
        speed_list = []
    
        for offset, sv in sv_pairs:
            while offset < bpm_pairs[0][0]:  # Offset cannot be less than the first bpm
                continue
            # Guarantee that svOffset is after first bpm
            if next_bpm_offset and offset >= next_bpm_offset:
                curr_bpm_iter += 1
                if curr_bpm_iter != len(bpm_pairs):
                    next_bpm_offset = bpm_pairs[curr_bpm_iter][0]
                else:
                    next_bpm_offset = None
            speed_list.append(dict(offset=offset, speed=bpm_pairs[curr_bpm_iter][1] * sv / center_bpm))
    
        return speed_list

    # noinspection PyMethodOverriding
    def metadata(self, unicode=True) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return:
        """

        def formatting(artist, title, difficulty, creator):
            return f"{artist} - {title}, {difficulty} ({creator})"

        return formatting(self.artist, self.title, self.version, self.creator)

    def rate(self, by: float, inplace:bool = False):
        """ Changes the rate of the map

        :param by: The value to rate it by. 1.1x speeds up the song by 10%. Hence 10/11 of the length.
        :param inplace: Whether to perform the operation in place. Returns a copy if False
        """
        this = self if inplace else self.deepcopy()
        super(DmMap, this).rate(by=by, inplace=True)

        return None if inplace else this
