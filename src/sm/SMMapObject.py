from src.base.MapObject import MapObject
from src.sm.SMMapObjectMeta import SMMapObjectMeta
from dataclasses import dataclass


@dataclass
class SMMapObject(MapObject, SMMapObjectMeta):

    def readFile(self, filePath: str):
        with open(filePath, "r") as f:
            file = f.read()
            fileSpl = file.split("\n")
            self._readMetadata(fileSpl[0:fileSpl.index("#NOTES:")])
            self._readNoteMetadata(fileSpl[fileSpl.index("#NOTES:")+1:fileSpl.index("#NOTES:")+6])
            self.hitObjects = self._readNotes(fileSpl[fileSpl.index("#NOTES:")+6:])

    def writeFile(self, filePath: str):
        pass

