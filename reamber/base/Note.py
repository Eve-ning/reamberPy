from reamber.base.Property import item_props
from reamber.base.Timed import Timed


@item_props()
class Note(Timed):
    """A Note Object is an abstract playable timed-object

    Do not get confused with Hit Object, which is just a single hit/tap.

    Hit != Note to make it clear on what is a note, hit and hold.
    """
    _props = dict(column=['int', 0])

    def __init__(self, offset: float, column: int, **kwargs):
        super().__init__(offset=offset, column=column, **kwargs)
