from __future__ import annotations

from reamber.base.Note import Note


class HoldTail(Note):
    """ The purpose of this class is to be able to detect the tail as a separate object instead of just Hold

    This class however, is entirely disconnected from Hold, and should only be used for convenience as using the head
    is more natural.
    """
    def __init__(self, offset: float, column: int, length: float, **kwargs):
        super(HoldTail, self).__init__(offset=offset, column=column, length=length, **kwargs)

    @property
    def length(self):
        return self.data['length']

    @length.setter
    def length(self, value):
        self.data['length'] = value

    @staticmethod
    def _from_series_allowed_names():
        return [*Note._from_series_allowed_names(), 'length']

class Hold(Note):
    """ A holdable timed object with a specified length.

    We only store the length, the tail offset is calculated.

    We don't directly inherit Hit because the inheritance may be confusing, we'll just subclass Note.
    """

    def __init__(self, offset: float, column: int, length: float, **kwargs):
        super(Hold, self).__init__(offset=offset, column=column, length=length, **kwargs)

    @property
    def length(self):
        return self.data['length']

    @length.setter
    def length(self, val):
        self.data['length'] = val

    @property
    def tail_offset(self) -> float:
        """ Gets the offset for the tail """
        return self.offset + self.length

    @staticmethod
    def _from_series_allowed_names():
        return [*Note._from_series_allowed_names(), 'length']
