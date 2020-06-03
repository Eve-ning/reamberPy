from __future__ import annotations
from typing import List, Tuple, overload, Type
from reamber.base.NoteObject import NoteObject
from reamber.base.HitObject import HitObject
from reamber.base.HoldObject import HoldObject
from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame


class MapObjectNotes(List[NoteObject], MapObjectGeneric, MapObjectDataFrame):

    def __init__(self, *args):
        list.__init__(self, *args)

    def data(self) -> List[NoteObject]:
        return self

    def maxCol(self) -> int:
        """ CALCULATES the key of the map
        Note that keys of the map isn't stored, it's dynamic and not a stored parameter.
        The function just finds the maximum column.
        """
        return max(self.columns())

    def columns(self):
        return [obj.column for obj in self.data()]

    def isColumns(self, columns: List[int]) -> MapObjectNotes:
        """ Gets all objects that are in these columns """
        return MapObjectNotes([obj for obj in self.data() if obj.column in columns])

    @overload
    def instances(self, instanceOf: Type[HitObject]) -> MapObjectGeneric: ...

    @overload
    def instances(self, instanceOf: Type[HoldObject]) -> MapObjectGeneric: ...

    def instances(self, instanceOf) -> MapObjectGeneric:
        return super().instances(instanceOf)

    def hits(self, sort: bool = False) -> List[HitObject]:
        """ Returns a copy of (Sorted) HitObjs """
        return self.instances(HitObject).sorted().data() if sort else \
               self.instances(HitObject).data()

    def holds(self, sort: bool = False) -> List[HoldObject]:
        """ Returns a copy of (Sorted) HoldObjs """
        return self.instances(HoldObject).sorted().data() if sort else \
               self.instances(HoldObject).data()

    def hitOffsets(self, sort: bool = True) -> List[float]:
        """ Returns a copy of the HitObj Offsets """
        return self.instances(HitObject).sorted().offsets() if sort else \
               self.instances(HitObject).offsets()

    def holdOffsets(self, sort: bool = True) -> List[Tuple[float, float]]:
        """ Returns a copy of the HoldObj Offsets [(Head0, Tail0), (Head1, Tail1), ...] """
        return [(ho.offset, ho.tailOffset()) for ho in self.instances(HoldObject).sorted().data()] if sort else \
               [(ho.offset, ho.tailOffset()) for ho in self.instances(HoldObject).data()]

    def lastOffset(self) -> float:
        """ Get Last Note Offset """
        hos = self.sorted()
        lastHit = self.hits()[-1]
        lastHold = self.holds()[-1]

        if lastHit.offset > lastHold.offset + lastHold.length:
            return lastHit.offset
        else:
            return lastHold.offset + lastHold.length

    def firstLastOffset(self) -> Tuple[float, float]:
        """ Get First and Last Note Offset
        This is slightly faster than separately calling the singular functions since it sorts once only
        """
        hos = self.sorted()
        lastHit = self.hits()[-1]
        lastHold = self.holds()[-1]

        if lastHit.offset > lastHold.offset + lastHold.length:
            return hos[0].offset, lastHit.offset
        else:
            return hos[0].offset, lastHold.offset + lastHold.length
