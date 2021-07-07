from typing import List

from reamber.base.Bpm import Bpm
from reamber.quaver.QuaMap import QuaMap
from reamber.sm.SMBpm import SMBpm
from reamber.sm.SMHit import SMHit
from reamber.sm.SMHold import SMHold
from reamber.sm.SMMapMeta import SMMapChartTypes
from reamber.sm.SMMapSet import SMMapSet, SMMap
from reamber.sm.lists.SMBpmList import SMBpmList
from reamber.sm.lists.SMNotePkg import SMNotePkg
from reamber.sm.lists.notes.SMHitList import SMHitList
from reamber.sm.lists.notes.SMHoldList import SMHoldList


class QuaToSM:
    @staticmethod
    def convert(qua: QuaMap) -> SMMapSet:
        """ Converts a Quaver map to a SMMapset Obj

        Note that each qua map object will create a separate mapset, they are not merged

        :param qua:
        :return:
        """
        hits: List[SMHit] = []
        holds: List[SMHold] = []

        for hit in qua.notes.hits():
            hits.append(SMHit(offset=hit.offset, column=hit.column))
        for hold in qua.notes.holds():
            holds.append(SMHold(offset=hold.offset, column=hold.column, _length=hold.length))

        bpms: List[Bpm] = []

        for bpm in qua.bpms:
            bpms.append(SMBpm(offset=bpm.offset, bpm=bpm.bpm))

        smSet: SMMapSet = SMMapSet(
            music=qua.audio_file,
            title=qua.title,
            titleTranslit=qua.title,
            artist=qua.artist,
            artistTranslit=qua.artist,
            credit=qua.creator,
            background=qua.background_file,
            sampleStart=qua.song_preview_time,
            sampleLength=10,
            offset=qua.notes.first_offset(),
            maps=[
                SMMap(
                    chartType=SMMapChartTypes.DANCE_SINGLE,
                    notes=SMNotePkg(hits=SMHitList(hits),
                                    holds=SMHoldList(holds)),
                    bpms=SMBpmList(bpms)
                )
            ]
        )

        return smSet
