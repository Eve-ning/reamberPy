from reamber.quaver.QuaMapObjMeta import QuaMapObjMeta
from reamber.base.MapObj import MapObj
from reamber.quaver.QuaSvObj import QuaSvObj
from reamber.quaver.QuaBpmObj import QuaBpmObj
from reamber.quaver.QuaHitObj import QuaHitObj
from reamber.quaver.QuaHoldObj import QuaHoldObj
from dataclasses import dataclass, field
from typing import List, Dict, Union
import yaml

from reamber.quaver.lists.QuaNotePkg import QuaNotePkg
from reamber.quaver.lists.QuaBpmList import QuaBpmList
from reamber.quaver.lists.QuaSvList import QuaSvList


@dataclass
class QuaMapObj(QuaMapObjMeta, MapObj):

    notes: QuaNotePkg = field(default_factory=lambda: QuaNotePkg())
    bpms:  QuaBpmList  = field(default_factory=lambda: QuaBpmList())
    svs:   QuaSvList   = field(default_factory=lambda: QuaSvList())

    def readFile(self, filePath: str):
        with open(filePath, "r", encoding="utf8") as f:
            file = yaml.safe_load(f)
        # We pop them so as to reduce the size needed to pass to _readMeta
        self._readNotes(file.pop('HitObjs'))
        self._readBpms(file.pop('TimingPoints'))
        self._readSVs(file.pop('SliderVelocities'))
        self._readMetadata(file)

    def writeFile(self, filePath: str):
        file = self._writeMeta()

        bpm: QuaBpmObj
        file['TimingPoints'] = [bpm.asDict() for bpm in self.bpms]
        sv: QuaSvObj
        file['SliderVelocities'] = [sv.asDict() for sv in self.svs]
        note: Union[QuaHitObj, QuaHoldObj]
        file['HitObjs'] = [note.asDict() for note in self.notes.data()]
        with open(filePath, "w+", encoding="utf8") as f:
            f.write(yaml.safe_dump(file, default_flow_style=False, sort_keys=False))

    def _readBpms(self, bpms: List[Dict]):
        for bpm in bpms:
            self.bpms.append(QuaBpmObj(offset=bpm['StartTime'], bpm=bpm['Bpm']))

    def _readSVs(self, svs: List[Dict]):
        for sv in svs:
            self.svs.append(QuaSvObj(offset=sv['StartTime'], multiplier=sv['Multiplier']))

    def _readNotes(self, notes: List[Dict]):
        for note in notes:
            offset = note['StartTime']
            column = note['Lane'] - 1
            keySounds = note['KeySounds']
            if "EndTime" in note.keys():
                self.notes.holds().append(QuaHoldObj(offset=offset, length=note['EndTime'] - offset,
                                                      column=column, keySounds=keySounds))
            else:
                self.notes.hits().append(QuaHitObj(offset=offset, column=column, keySounds=keySounds))
