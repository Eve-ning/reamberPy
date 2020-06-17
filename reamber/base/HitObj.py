from reamber.base.NoteObj import NoteObj
from dataclasses import dataclass


@dataclass
class HitObj(NoteObj):
    """ A Hit Object is a timed object that is just a single tap

    Do not get confused with Note Object, which describes both hit and holds.
    """
    pass
