""" The purpose of having separate classes for these objects is to facilitate functions that deal with the whole list
E.g.
Instead of having to do a for loop to shift offset ...
    for obj in map:
        obj.offset += 100

We can just call a function
    map.notes.addOffset(100)

There are also other helper classifiers such as MapObjectDataFrame, which indicates that the class can be coerced into
a pandas DataFrame.

Convention
When inheriting from this, place everything in mapobj package.
Names inheriting should be plural, to be clear
Also, inherit from the List[Obj] with the appropriate __init__

E.g. class MapObjectBpms(List[BpmPoint], MapObjectGeneric, ...)
        def __init__(self, *args):
            list.__init__(self, *args)

Unlike most things in the repository, this is not a @dataclass

"""

from reamber.base.mapobj.MapObjectDataFrame import MapObjectDataFrame
from reamber.base.mapobj.MapObjectBpms import MapObjectBpms
from reamber.base.mapobj.MapObjectGeneric import MapObjectGeneric
from reamber.base.mapobj.MapObjectNotes import MapObjectNotes

__all__ = ['MapObjectDataFrame', 'MapObjectBpms', 'MapObjectGeneric', 'MapObjectNotes']
