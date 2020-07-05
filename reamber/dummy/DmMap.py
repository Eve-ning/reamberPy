from reamber.dummy.DmMapMeta import DmMapMeta
from reamber.base.Map import Map
from reamber.dummy.lists.DmSvList import DmSvList

from reamber.dummy.DmBpm import DmBpm
from reamber.dummy.DmSv import DmSv
from reamber.dummy.DmHit import DmHit
from reamber.dummy.DmHold import DmHold

from typing import List, Dict
from dataclasses import dataclass, field

from reamber.dummy.lists.DmNotePkg import DmNotePkg
from reamber.dummy.lists.DmBpmList import DmBpmList
from reamber.base.lists.TimedList import TimedList

@dataclass
class DmMap(Map, DmMapMeta):

    notes: DmNotePkg = field(default_factory=lambda: DmNotePkg())
    bpms:  DmBpmList = field(default_factory=lambda: DmBpmList())
    svs:   DmSvList  = field(default_factory=lambda: DmSvList())

    def initHits(self,
                 noteCols: List[int],
                 noteOffsets: List[float]):

        assert len(noteCols) == len(noteOffsets), "Note Cols and Offset lengths must match."
        hits = self.notes.hits()
        [hits.append(DmHit(column=col, offset=offset)) for col, offset in zip(noteCols, noteOffsets)]

    def initHolds(self,
                  noteCols: List[int],
                  noteOffsets: List[float],
                  noteLengths: List[float]):

        assert len(noteCols) == len(noteOffsets) == len(noteLengths), "Note Cols, offset, length lengths must match."
        holds = self.notes.holds()
        [holds.append(DmHold(column=col, offset=offset, length=length))
         for col, offset, length in zip(noteCols, noteOffsets, noteLengths)]

    def initBpms(self,
                 bpms: List[float],
                 bpmsOffsets: List[float]):

        assert len(bpms) == len(bpmsOffsets), "Note Cols, offset, length lengths must match."
        [self.bpms.append(DmBpm(bpm=bpm, offset=offset)) for bpm, offset in zip(bpms, bpmsOffsets)]

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes, bpms and svs as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms,
                'svs': self.svs}

    def scrollSpeed(self, centerBpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType. Overrides the base to include SV
    
        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param centerBpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """
    
        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if centerBpm is None: centerBpm = 1
    
        svPairs = [(offset, multiplier) for offset, multiplier in zip(self.svs.sorted().offsets(),
                                                                      self.svs.multipliers())]
        bpmPairs = [(offset, bpm) for offset, bpm in zip(self.bpms.offsets(), self.bpms.bpms())]
    
        currBpmIter = 0
        nextBpmOffset = None if len(bpmPairs) == 1 else bpmPairs[1][0]
        speedList = []
    
        for offset, sv in svPairs:
            while offset < bpmPairs[0][0]:  # Offset cannot be less than the first bpm
                continue
            # Guarantee that svOffset is after first bpm
            if nextBpmOffset and offset >= nextBpmOffset:
                currBpmIter += 1
                if currBpmIter != len(bpmPairs):
                    nextBpmOffset = bpmPairs[currBpmIter][0]
                else:
                    nextBpmOffset = None
            speedList.append(dict(offset=offset, speed=bpmPairs[currBpmIter][1] * sv / centerBpm))
    
        return speedList

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
