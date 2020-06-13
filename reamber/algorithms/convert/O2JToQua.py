from reamber.o2jam.O2JMapSetObj import O2JMapSetObj, O2JMapObj
from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.quaver.QuaHitObj import QuaHitObj
from reamber.quaver.QuaHoldObj import QuaHoldObj
from reamber.quaver.QuaBpmObj import QuaBpmObj
from reamber.base.BpmObj import BpmObj
from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.notes.QuaHoldList import QuaHoldList
from reamber.quaver.lists.notes.QuaHitList import QuaHitList
from typing import List


class O2JToQua:
    @staticmethod
    def convert(o2j: O2JMapSetObj) -> List[QuaMapObj]:
        """ Converts a Mapset to possibly multiple quaver maps
        Note that a mapset contains maps, so a list would be expected.
        O2JMap conversion is not possible due to lack of O2JMapset Metadata
        :param o2j: The MapSet
        :return: Quaver Maps
        """
        quaMapSet: List[QuaMapObj] = []
        for o2jm in o2j.maps:
            assert isinstance(o2jm, O2JMapObj)
            hits: List[QuaHitObj] = []
            holds: List[QuaHoldObj] = []

            # Note Conversion
            for hit in o2jm.notes.hits():
                hits.append(QuaHitObj(offset=hit.offset, column=hit.column))
            for hold in o2jm.notes.holds():
                holds.append(QuaHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

            bpms: List[BpmObj] = []

            # Timing Point Conversion
            for bpm in o2jm.bpms:
                bpms.append(QuaBpmObj(offset=bpm.offset, bpm=bpm.bpm))

            # Extract Metadata
            quaMap = QuaMapObj(
                title=o2j.title,
                artist=o2j.artist,
                creator=o2j.creator,
                difficultyName=f"Level {o2j.level[o2j.maps.index(o2jm)]}",
                bpms=QuaBpmList(bpms),
                notes=QuaNotePkg(hits=QuaHitList(hits),
                                 holds=QuaHoldList(holds))
            )
            quaMapSet.append(quaMap)
        return quaMapSet
