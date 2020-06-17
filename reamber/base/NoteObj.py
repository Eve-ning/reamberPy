from dataclasses import dataclass
from reamber.base.TimedObj import TimedObj


@dataclass
class NoteObj(TimedObj):
    """ A Note Object is a playable timed object

    Do not get confused with Hit Object, which is just a single hit/tap.

    The naming convention is done this way to make it clear on what is a note, hit and hold.
    """
    column: int = 0
