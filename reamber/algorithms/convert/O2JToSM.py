from typing import List

from reamber.base.Bpm import Bpm
from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMHit import SMHit
from reamber.sm.SMHold import SMHold
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class O2JToSM:
    @staticmethod
    def convert(o2j: O2JMapSet) -> List[SMMapSet]:
        """ Converts a Mapset to multiple SM maps

        Due to non-confidence that bpms are consistent, A list of SMSet would be generated.

        :param o2j:
        :return:
        """

        smSets = []

        for o2jMap in o2j.maps:

            bpms: List[Bpm] = []
            for bpm in o2jMap.bpms:
                bpms.append(SMBpm(offset=bpm.offset, bpm=bpm.bpm))

            hits: List[SMHit] = []
            holds: List[SMHold] = []

            for hit in o2jMap.notes.hits():
                hits.append(SMHit(offset=hit.offset, column=hit.column))
            for hold in o2jMap.notes.holds():
                holds.append(SMHold(offset=hold.offset, column=hold.column, _length=hold.length))

            smSet: SMMapSet = SMMapSet(
                title=o2j.title,
                artist=o2j.artist,
                credit=o2j.creator,
                offset=0.0,
                maps=[
                    SMMap(
                        description=f"Level {o2j.level[o2j.maps.index(o2jMap)]}",
                        chartType=SMMapChartTypes.KB7_SINGLE,
                        notes=SMNotePkg(hits=SMHitList(hits),
                                        holds=SMHoldList(holds)),
                        bpms=SMBpmList(bpms)
                    )
                ]
            )
            smSets.append(smSet)

        return smSets
