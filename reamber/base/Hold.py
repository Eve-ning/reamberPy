from __future__ import annotations
from reamber.base.Note import Note
from typing import Type
from dataclasses import dataclass, InitVar, field, asdict, is_dataclass
from abc import abstractmethod


@dataclass
class HoldTail(Note):
    """ The purpose of this class is to be able to detect the tail as a separate object instead of just Hold """
    pass


@dataclass
class Hold(Note):
    """ A holdable timed object with a specified length.

    We only store the length, the tail offset is calculated. """

    # We name it like this so the constructor is clearer
    _length: InitVar[float] = 0.0
    tail: HoldTail = field(init=False)  # [OVERRIDE] this so that the property gets the correct type

    @abstractmethod
    def _upcastTail(self, **kwargs) -> HoldTail:
        """ Required method to override, to implement own HoldTails.

        It will take the same arguments as this inherited class excluding _length.

        e.g. return HoldTail(**kwargs)
        """
        ...

    @classmethod
    def fromAnother(cls: Type[Hold], other: Hold or dict):
        d = asdict(other)
        d['_length'] = d['tail']['offset'] - other.offset
        d.pop('tail')
        return cls(**d)

    @classmethod
    def fromDict(cls: Type[Hold], other: dict):
        d = other
        d['_length'] = d['tail']['offset'] - other['offset']
        d.pop('tail')
        return cls(**d)

    def __post_init__(self, _length: float):
        # noinspection PyTypeChecker
        # dataclasses throws an error if tail is not defined, we just use None, we don't need it anyways.
        self.tail = None
        d = asdict(self)
        d.pop("tail")
        d['offset'] += _length
        self.tail = self._upcastTail(**d)

    @property
    def length(self):
        return self.tailOffset() - self.offset

    @length.setter
    def length(self, val: float):
        self.tail.offset = self.offset + val

    def tailOffset(self) -> float:
        """ Gets the offset for the tail """
        return self.tail.offset

    def multOffset(self, by: float, inplace:bool = False):
        this = self if inplace else self.deepcopy()
        this.offset *= by
        this.length *= by
        return None if inplace else this

