from __future__ import annotations

from reamber.base.Note import Note
from reamber.base.Property import item_props


@item_props()
class HoldTail(Note):
    """A dummy class for tail detection APIs

    ``HoldTail`` is entirely independent of ``Hold``.

    Notes:
        This is currently only used in the ``Pattern`` algorithm
    """

    _props = dict(length=['float', 0.0])

    def __init__(self, offset: float, column: int, length: float, **kwargs):
        """Initializer

        Args:
            offset: Offset in ms
            column: Column of Tail, should be same as ``Hold``
            length: Length of Hold, should be same as ``Hold``
        """
        super().__init__(offset=offset, column=column, length=length, **kwargs)


@item_props()
class Hold(Note):
    """A held timed object with a length.

    Notes:
        We only store the length, the tail offset is calculated.
        We inherit ``Note`` instead of ``Hit``

    Examples:

        >>> h = Hold(offset=1000, column=1, length=1000)
        >>> h.tail_offset
        2000
    """

    _props = dict(length=['float', 0.0])

    def __init__(self, offset: float, column: int, length: float, **kwargs):
        """Initializer

        Args:
            offset: Offset in ms
            column: Column
            length: Length in ms
        """
        super().__init__(offset=offset, column=column, length=length, **kwargs)

    @property
    def tail_offset(self) -> float:
        """Offset of the tail in ms

        Notes:
            This is simply ``offset`` + ``length``

        Returns:
            ``float`` of Tail offset in ms

        """
        return self.offset + self.length
