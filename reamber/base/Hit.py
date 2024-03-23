from reamber.base.Note import Note
from reamber.base.Property import item_props


@item_props()
class Hit(Note):
    """A Hit Object is a timed object that is just a single tap

    Do not get confused with Note Object, which describes both hit and holds.

    Examples:

        >>> h = Hit(offset=1000, column=1)
        >>> h.offset
        1000
    """

    ...
