from reamber.base.Note import Note
from dataclasses import dataclass


@dataclass
class Hit(Note):
    """ A Hit Object is a timed object that is just a single tap

    Do not get confused with Note Object, which describes both hit and holds.
    """
    pass
