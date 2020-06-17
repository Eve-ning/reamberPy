from reamber.sm.SMMapSetObj import SMMapSetObj, SMMapObj
from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
from reamber.base.BpmObj import BpmObj
from reamber.sm.SMMapObjMeta import SMMapObjChartTypes
from reamber.sm.SMHitObj import SMHitObj
from reamber.sm.SMHoldObj import SMHoldObj
from reamber.sm.SMBpmObj import SMBpmObj
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList
from typing import List


class O2JToSM:
    @staticmethod
    def convert(o2j: O2JMapSetObj) -> List[SMMapSetObj]:
        """ Converts a Mapset to multiple SM maps

        Due to non-confidence that bpms are consistent, A list of SMSet would be generated.

        :param o2j: O2Jam Mapset
        :return: List of SM MapSets
        """

        smSets = []

        for o2jMap in o2j.maps:

            bpms: List[BpmObj] = []
            for bpm in o2jMap.bpms:
                bpms.append(SMBpmObj(offset=bpm.offset, bpm=bpm.bpm))

            hits: List[SMHitObj] = []
            holds: List[SMHoldObj] = []

            for hit in o2jMap.notes.hits():
                hits.append(SMHitObj(offset=hit.offset, column=hit.column))
            for hold in o2jMap.notes.holds():
                holds.append(SMHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

            smSet: SMMapSetObj = SMMapSetObj(
                title=o2j.title,
                artist=o2j.artist,
                credit=o2j.creator,
                offset=0.0,
                maps=[
                    SMMapObj(
                        description=f"Level {o2j.level[o2j.maps.index(o2jMap)]}",
                        chartType=SMMapObjChartTypes.KB7_SINGLE,
                        notes=SMNotePkg(hits=SMHitList(hits),
                                        holds=SMHoldList(holds)),
                        bpms=SMBpmList(bpms)
                    )
                ]
            )
            smSets.append(smSet)

        return smSets
