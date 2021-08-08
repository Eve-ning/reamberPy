from typing import List

from reamber.algorithms.convert.ConvertBase import ConvertBase
from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.sm import SMMap
from reamber.sm.SMMapSet import SMMapSet
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class O2JToSM(ConvertBase):
    @classmethod
    def convert(cls, o2js: O2JMapSet) -> List[SMMapSet]:
        """ Converts a Mapset to multiple SM maps

        Due to non-confidence that bpms are consistent, A list of SMSet would be generated.

        If you're certain to merge them, use convert_merge."""

        smss = []

        for o2j in o2js:
            sms = SMMapSet()
            sm = SMMap()
            sm.hits = cls.cast(o2j.hits, SMHitList, dict(offset='offset', column='column'))
            sm.holds = cls.cast(o2j.holds, SMHoldList, dict(offset='offset', column='column', length='length'))
            sm.bpms = cls.cast(o2j.bpms, SMBpmList, dict(offset='offset', bpm='bpm'))

            sms.maps = [sm]

            sms.title = o2js.title
            sms.artist = o2js.artist
            sms.credit = o2js.creator
            sms.offset = 0.0

            smss.append(sms)

        return smss

    @classmethod
    def convert_merge(cls, o2js: O2JMapSet) -> SMMapSet:
        """ Converts a Mapset to a single SM mapset.

        If the bpms are not consistent, this can cause a corrupted SMMapSet."""

        sms = SMMapSet()

        for o2j in o2js:
            sms = SMMapSet()
            sm = SMMap()
            sm.hits = cls.cast(o2j.hits, SMHitList, dict(offset='offset', column='column'))
            sm.holds = cls.cast(o2j.holds, SMHoldList, dict(offset='offset', column='column', length='length'))
            sm.bpms = cls.cast(o2j.bpms, SMBpmList, dict(offset='offset', bpm='bpm'))

            sms.maps.append(sm)

        sms.title = o2js.title
        sms.artist = o2js.artist
        sms.credit = o2js.creator
        sms.offset = 0.0

        return sms
