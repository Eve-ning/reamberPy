from reamber.quaver.QuaMapObjectMeta import QuaMapObjectMeta
from reamber.base.MapObject import MapObject
from reamber.quaver.QuaSliderVelocity import QuaSliderVelocity
from reamber.quaver.QuaBpmPoint import QuaBpmPoint
from reamber.quaver.QuaHitObject import QuaHitObject
from reamber.quaver.QuaHoldObject import QuaHoldObject
from dataclasses import dataclass, field
from typing import List, Dict, Union
import yaml


@dataclass
class QuaMapObject(QuaMapObjectMeta, MapObject):
    svPoints: List[QuaSliderVelocity] = field(default_factory=lambda: [])

    def readFile(self, filePath: str):
        with open(filePath, "r", encoding="utf8") as f:
            file = yaml.safe_load(f)
        # We pop them so as to reduce the size needed to pass to _readMeta
        self._readNotes(file.pop('HitObjects'))
        self._readBpms(file.pop('TimingPoints'))
        self._readSVs(file.pop('SliderVelocities'))
        self._readMetadata(file)

    def writeFile(self, filePath: str):
        file = self._writeMeta()

        bpm: QuaBpmPoint
        file['TimingPoints'] = [bpm.asDict() for bpm in self.bpmPoints]
        sv: QuaSliderVelocity
        file['SliderVelocities'] = [sv.asDict() for sv in self.svPoints]
        note: Union[QuaHitObject, QuaHoldObject]
        file['HitObjects'] = [note.asDict() for note in self.noteObjects]
        with open(filePath, "w+", encoding="utf8") as f:
            f.write(yaml.safe_dump(file, default_flow_style=False, sort_keys=False))

    def _readBpms(self, bpms: List[Dict]):
        for bpm in bpms:
            self.bpmPoints.append(QuaBpmPoint(offset=bpm['StartTime'], bpm=bpm['Bpm']))

    def _readSVs(self, svs: List[Dict]):
        for sv in svs:
            self.svPoints.append(QuaSliderVelocity(offset=sv['StartTime'], multiplier=sv['Multiplier']))

    def _readNotes(self, notes: List[Dict]):
        for note in notes:
            offset = note['StartTime']
            column = note['Lane'] - 1
            keySounds = note['KeySounds']
            if "EndTime" in note.keys():
                self.noteObjects.append(QuaHoldObject(offset=offset, length=note['EndTime'] - offset,
                                                      column=column, keySounds=keySounds))
            else:
                self.noteObjects.append(QuaHitObject(offset=offset, column=column, keySounds=keySounds))

