from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, TYPE_CHECKING

from reamber.base.Map import Map
from reamber.base.Property import map_props
from reamber.base.RAConst import RAConst
from reamber.base.lists import TimedList
from reamber.o2jam.O2JBpm import O2JBpm
from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.O2JHit import O2JHit
from reamber.o2jam.O2JHold import O2JHold
from reamber.o2jam.lists.O2JBpmList import O2JBpmList
from reamber.o2jam.lists.notes import O2JNoteList
from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList

if TYPE_CHECKING:
    from reamber.o2jam.O2JMapSet import O2JMapSet

import logging

log = logging.getLogger(__name__)


@map_props()
@dataclass
class O2JMap(Map[O2JNoteList, O2JHitList, O2JHoldList, O2JBpmList]):
    """This holds a single level of a .ojn file out of a total of three.

    This class only holds the data of notes and bpms. The rest can be found in
    the parent O2JMapSet instance.

    We won't support OJM, see why in O2JMapSet. """

    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(hits=O2JHitList([]),
                                           holds=O2JHoldList([]),
                                           bpms=O2JBpmList([])))

    # noinspection PyUnresolvedReferences
    @staticmethod
    def read_pkgs(pkgs: List[O2JEventPackage], init_bpm: float) -> O2JMap:
        """Reads a level/map package and returns a O2JMap

        Args:
            pkgs: Packages read to be parsed
            init_bpm: Initial bpm for the map from the metadata
        """

        """
        We get unique measures from notes then find the offsets via bpm:
        
        We drop them into the events_note_dict:
        { 10: 300, 12: 5000 }

        Then we loop through the notes to obtain the correct offsets.

        We do this because we don't want to separate and pair the LNs again 
        since we have to go through this algorithm by a sorted offset.
        """
        events = [event for pkg in pkgs for event in pkg.events]
        events.sort(key=lambda x: x.measure)

        notes = [e for e in events if not isinstance(e, O2JBpm)]
        note_measures = {note.measure for note in notes} | \
                        {note.tail_measure for note in notes if
                         isinstance(note, O2JHold)}
        note_measures = sorted(note_measures)
        note_measure_dict = {}

        bpms = [e for e in events if isinstance(e, O2JBpm)]

        offset = 0
        measure = 0
        bpm_ix = -1
        bpm_val = init_bpm

        next_bpm_measure = bpms[0].measure if len(bpms) > 0 else None
        for note_measure in note_measures:
            if not next_bpm_measure:

                while note_measure > next_bpm_measure:
                    bpm_ix += 1
                    bpm = bpms[bpm_ix]
                    # Update offset
                    offset += RAConst.min_to_msec(
                        (bpm.measure - measure) * 4 / bpm_val
                    )
                    bpm.offset = offset
                    measure = bpm.measure
                    bpm_val = bpm.bpm

                    # Check if next one is available
                    if bpm_ix + 1 == len(bpms):
                        next_bpm_measure = None
                        break
                    else:
                        next_bpm_measure = bpm.measure

            # We add it into the measure: offset dictionary.
            note_measure_dict[note_measure] = \
                offset + \
                RAConst.min_to_msec(4 * (note_measure - measure) / bpm_val)

        # We then assign all the offsets here
        for note in notes:
            note.offset = note_measure_dict[note.measure]
            if isinstance(note, O2JHold):  # Special case for LN.
                note.length = note_measure_dict[note.tail_measure] - \
                              note.offset

        # We add the missing first BPM here
        bpms.insert(0, O2JBpm(offset=0, bpm=init_bpm))
        m = O2JMap()
        m.hits = O2JHitList([n for n in notes if isinstance(n, O2JHit)])
        m.holds = O2JHoldList([n for n in notes if isinstance(n, O2JHold)])
        m.bpms = O2JBpmList(bpms)
        return m

    # noinspection PyMethodOverriding
    # Class requires set to operate
    def metadata(self, s: O2JMapSet, unicode=True) -> str:
        """Grabs the map metadata

        Notes:
            This doesn't try to convert unicode to ascii.

        Args:
            s: The Map Set Object, required for additional metadata info.
            unicode: Whether to use unicode if available.

        Returns:
            A string containing the metadata
        """

        fmt = "{} - {}, {} ({})"

        try:
            return fmt.format(s.artist.strip(), s.title,
                              f"Level {s.level_name(self)}", s.creator)
        except IndexError:
            return fmt.format(s.artist, s.title, "Cannot determine level",
                              s.creator)

    # noinspection PyMethodOverriding
    def describe(self, s: O2JMapSet, rounding: int = 2,
                 unicode: bool = False) -> str:
        """Describes the map's attributes as a short summary

        Args:
            s: The Map Set Object, required for additional metadata info.
            rounding: The decimal rounding
            unicode: Whether to attempt to get the non-unicode or unicode.
                Doesn't attempt to translate.
        """
        return super().describe(rounding=rounding, unicode=unicode, s=s)
