from __future__ import annotations
from dataclasses import dataclass, field

from reamber.base.Map import Map
from reamber.base.RAConst import RAConst
from reamber.base.lists import TimedList
from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.lists.O2JNotePkg import O2JNotePkg
from reamber.o2jam.lists.O2JBpmList import O2JBpmList, O2JBpm
from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList
from reamber.o2jam.O2JHit import O2JHit
from reamber.o2jam.O2JHold import O2JHold
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from reamber.o2jam.O2JMapSet import O2JMapSet

import logging

log = logging.getLogger(__name__)

@dataclass
class O2JMap(Map):
    """ This holds a single level of a .ojn file out of a total of three.

    This class only holds the data of notes and bpms. The rest can be found in the parent O2JMapSet instance.

    We won't support OJM, see why in O2JMapSet. """

    notes: O2JNotePkg = field(default_factory=lambda: O2JNotePkg())
    bpms:  O2JBpmList = field(default_factory=lambda: O2JBpmList())

    def data(self) -> Dict[str, TimedList]:
        """ Gets the notes and bpms as a dictionary """
        return {'notes': self.notes,
                'bpms': self.bpms}

    # noinspection PyUnresolvedReferences
    @staticmethod
    def readPkgs(pkgs: List[O2JEventPackage], initBpm: float) -> O2JMap:
        """ Reads a level/map package and returns a O2JMap

        :param pkgs: A map package
        :param initBpm: The initial bpm for the map, it's the one located in the meta
        :return:
        """

        """ The main idea here is to get unique measures from notes and find out the real offsets via bpm
        The catch is that we drop them into the eventsNoteDict as a dictionary like
        { 10: 300, 12: 5000 }

        Then we loop through the notes to obtain the correct offsets.

        We do this because we don't want to separate and pair the LNs again since we have to go through this
        algorithm by a sorted offset.
        """
        events = [event for pkg in pkgs for event in pkg.events]
        events.sort(key=lambda x: x.measure)
        notes = [event for event in events if not isinstance(event, O2JBpm)]
        noteMeasures = {event.measure for event in notes} | \
                       {event.tailMeasure for event in notes if isinstance(event, O2JHold)}
        noteMeasures = sorted(noteMeasures)
        noteMeasureDict = {}
        bpms = [event for event in events if isinstance(event, O2JBpm)]

        currOffset = 0
        currMeasure = 0
        currBpmI = -1
        currBpm = initBpm
        nextBpmMeasure = bpms[0].measure if len(bpms) > 0 else None
        for noteMeasure in noteMeasures:
            if nextBpmMeasure:
                while noteMeasure > nextBpmMeasure:
                    # Move BPM Index up by 1
                    currBpmI += 1

                    # Update offset
                    currOffset += RAConst.minToMSec((bpms[currBpmI].measure - currMeasure) * 4 / currBpm)
                    bpms[currBpmI].offset = currOffset
                    currMeasure = bpms[currBpmI].measure
                    currBpm = bpms[currBpmI].bpm

                    # Check if next one is available
                    if currBpmI + 1 == len(bpms):
                        nextBpmMeasure = None
                        break
                    else:
                        nextBpmMeasure = bpms[currBpmI + 1].measure

            # We add it into the measure: offset dictionary.
            noteMeasureDict[noteMeasure] = \
                currOffset + RAConst.minToMSec(4 * (noteMeasure - currMeasure) / currBpm)

        # We then assign all the offsets here
        for note in notes:
            note.offset = noteMeasureDict[note.measure]
            if isinstance(note, O2JHold):  # Special case for LN.
                note.length = noteMeasureDict[note.tailMeasure] - note.offset

        # We add the missing first BPM here
        bpms.insert(0, O2JBpm(offset=0, bpm=initBpm))
        return O2JMap(notes=O2JNotePkg(hits=O2JHitList([n for n in notes if isinstance(n, O2JHit)]),
                                          holds=O2JHoldList([n for n in notes if isinstance(n, O2JHold)])),
                         bpms=O2JBpmList(bpms))

    # noinspection PyMethodOverriding
    # Class requires set to operate
    def metadata(self, s: O2JMapSet, unicode=True) -> str:
        """ Grabs the map metadata

        :param s: The Map Set Object, required for additional metadata info.
        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return:
        """

        def formatting(artist, title, difficulty, creator):
            return f"{artist} - {title}, {difficulty} ({creator})"

        try:
            return formatting(s.artist.strip(), s.title, f"Level {s.level[s.maps.index(self)]}", s.creator)
        except IndexError:
            return formatting(s.artist, s.title, "Cannot determine level", s.creator)

    # noinspection PyMethodOverriding
    def describe(self, s:O2JMapSet, rounding: int = 2, unicode: bool = False) -> None:
        """ Describes the map's attributes as a short summary

        :param s: The Map Set Object, required for additional metadata info.
        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """
        super(O2JMap, self).describe(rounding=rounding, unicode=unicode, s=s)
