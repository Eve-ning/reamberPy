from reamber.quaver.QuaMapObj import QuaMapObj
from reamber.quaver.QuaMapObjMeta import QuaMapObjMode
from reamber.osu.OsuMapObj import OsuMapObj
from reamber.osu.OsuHitObj import OsuHitObj
from reamber.osu.OsuHoldObj import OsuHoldObj
from reamber.osu.OsuBpmObj import OsuBpmObj
from reamber.osu.OsuSvObj import OsuSvObj
from reamber.base.BpmObj import BpmObj

from reamber.osu.lists.OsuBpmList import OsuBpmList
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList
from reamber.osu.lists.notes.OsuHitList import OsuHitList
from reamber.osu.lists.OsuSvList import OsuSvList
from typing import List


class QuaToOsu:
    @staticmethod
    def convert(qua: QuaMapObj) -> OsuMapObj:
        """ Converts a Quaver map to an osu map

        :param qua: Quaver map
        :return: Osu Map
        """

        hits: List[OsuHitObj] = []
        holds: List[OsuHoldObj] = []

        # Note Conversion
        for hit in qua.notes.hits():
            hits.append(OsuHitObj(offset=hit.offset, column=hit.column))
        for hold in qua.notes.holds():
            holds.append(OsuHoldObj(offset=hold.offset, column=hold.column, length=hold.length))

        bpms: List[BpmObj] = []
        svs: List[OsuSvObj] = []
        # Timing Point Conversion
        for bpm in qua.bpms:
            bpms.append(OsuBpmObj(offset=bpm.offset, bpm=bpm.bpm))

        for sv in qua.svs:
            svs.append(OsuSvObj(offset=sv.offset, multiplier=sv.multiplier))

        # Extract Metadata
        osuMap = OsuMapObj(
            backgroundFileName=qua.backgroundFile,
            title=qua.title,
            circleSize=QuaMapObjMode.keys(qua.mode),
            titleUnicode=qua.title,
            artist=qua.artist,
            artistUnicode=qua.artist,
            audioFileName=qua.audioFile,
            creator=qua.creator,
            version=qua.difficultyName,
            previewTime=qua.songPreviewTime,
            bpms=OsuBpmList(bpms),
            svs=OsuSvList(svs),
            notes=OsuNotePkg(hits=OsuHitList(hits),
                             holds=OsuHoldList(holds))
        )

        return osuMap
