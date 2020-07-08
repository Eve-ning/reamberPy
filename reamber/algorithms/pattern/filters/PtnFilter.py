from __future__ import annotations
from typing import List
from itertools import permutations
import numpy as np

from dataclasses import dataclass


@dataclass
class PtnFilter:

    ar: np.ndarray
    invertFilter: bool = False

    def __and__(self, other: PtnFilter or np.ndarray):
        """ This finds the intersects of these 2 arrays

        The method used here is pretty interesting.

        1. We firstly convert self and other to structured arrays, this operation gives each entry a temp name.
        2. We then used intersect1d. This works because each entry is now treated as one entity
        3. We then extract everything by doing a single-index extraction with the names.

        The catch for single vs. multi index is that if you do multi-index, you'll end up extracting a structured array.

        """
        self_ = np.array(np.core.records.fromarrays(self.ar.transpose()))
        other_ = np.array(np.core.records.fromarrays(other.ar.transpose() if isinstance(other, PtnFilter)
                                                                          else other.transpose().astype('<i4')))

        # noinspection PyTypeChecker
        new_ = np.intersect1d(self_, other_)
        return PtnFilter(np.array([new_[n] for n in self_.dtype.names]).transpose())

    def __or__(self, other: PtnFilter or np.ndarray):
        """ This finds the union of these 2 arrays """

        # This is much easier to write :)
        return PtnFilter(np.unique(
            np.concatenate([self.ar, other.ar if isinstance(other, PtnFilter) else other.astype('<i4')], axis=0), axis=0))

    def filter(self, data): ...

class PtnFilterCombo(PtnFilter):
    """ This class helps generate a lambda fitting for passing it into combinations. """

    def filter(self, data: np.ndarray) -> np.ndarray:
        # [[0 1 2], [0 1 3]]
        self_ = np.array(np.core.records.fromarrays(self.ar.transpose()))
        other_ = np.array(np.core.records.fromarrays(data.transpose().astype('<i4')))
        return np.invert(np.isin(other_, self_)) if self.invertFilter else np.isin(other_, self_)

    class Method:
        """ The methods available to use in fromCombo
        
        Repeat just repeats the base pattern without changing its orientation.
        
        [0][1] --REPEAT-> [[0][1],[1][2],[2][3]] for keys=4
        
        Hmirror reflects the pattern on the y-axis
        
        [0][1] --HMIRROR-> [[0][1],[2][3]] for keys=4
        
        Vmirror reflects the pattern on the x-axis
        
        [0][1] --HMIRROR-> [[0][1],[1][0]] for keys=4
        
        """
        REPEAT: int = 2 ** 0
        HMIRROR: int = 2 ** 1
        VMIRROR: int = 2 ** 2

    @staticmethod
    def create(cols: List[List[int]], keys: int,
               method: Method or int = 0, invertFilter: bool = False) -> PtnFilterCombo:
        """ Generates alternate combos by just specifying a base combo
        
        Combos are implicitly distinct/unique and sorted on output.

        :param cols: The cols of the combo. e.g. ([1,2][3,4])
        :param keys: The keys of the map.
        :param method: Method to use, see PtnComboMethod. e.g. To use all methods:
            method=Method.VMIRROR | Method.HMIRROR | Method.REPEAT
        :param invertFilter: Whether to invert the filter, if True, these combos will be excluded
        :return:
        """
        cols_ = np.array(cols) if isinstance(cols, List) else cols
        if np.ndim(cols_) < 2: cols_ = np.expand_dims(cols, axis=list(range(2 - np.ndim(cols_))))

        if method & PtnFilterCombo.Method.REPEAT == PtnFilterCombo.Method.REPEAT:
            repeats = (keys - (np.max(cols_) - np.min(cols_)))
            cols_ = np.tile(cols_, (repeats, 1)) + \
                    np.repeat(
                        np.tile(np.expand_dims(np.arange(-np.min(cols_), -np.min(cols_) + repeats), axis=1),
                                (1, cols_.shape[1])), axis=0, repeats=cols_.shape[0])

        if method & PtnFilterCombo.Method.HMIRROR == PtnFilterCombo.Method.HMIRROR:
            mid = (keys - 1) / 2.0
            cols_ = np.concatenate([cols_, ((mid - cols_) * 2 + cols_).astype(int)])

        if method & PtnFilterCombo.Method.VMIRROR == PtnFilterCombo.Method.VMIRROR:
            cols_ = np.concatenate([cols_, np.flip(cols_, axis=[1])])

        return PtnFilterCombo(np.unique(cols_, axis=0), invertFilter)


class PtnFilterChord(PtnFilter):
    """ This class helps generate a lambda fitting for passing it into combinations. """

    def filter(self, data: np.ndarray) -> bool:
        # [[0 1 2], [0 1 3]]
        self_ = np.array(np.core.records.fromarrays(self.ar.transpose()))
        other_ = np.array(np.core.records.fromarrays(np.expand_dims(data, axis=0).transpose().astype('<i4')))
        return np.invert(np.alltrue(np.isin(other_, self_)))\
            if self.invertFilter else np.alltrue(np.isin(other_, self_))

    class Method:
        """ The methods available to use in fromChord

        Hmirror reflects the pattern on the y-axis

        [3][2][1] --HMIRROR-> [1][2][3]

        AnyPerm generates any chord sequences that is a combination of the current

        [2][2][1] --ANDLOWER-> [[2][2][1],[1][2][1],[2][1][1],[1][1][1]]

        AndLower generates any chord sequences that is lower than the current

        [2][2][1] --ANDLOWER-> [[2][2][1],[1][2][1],[2][1][1],[1][1][1]]
        
        AndHigher is just the opposite of AndLower

        """
        ANY_ORDER: int = 2 ** 0
        AND_LOWER: int = 2 ** 1
        AND_HIGHER: int = 2 ** 2

    @staticmethod
    def create(sizes: List[List[int]], keys:int, method: PtnFilterChord or int = 0,
               invertFilter:bool = False) -> PtnFilterChord:
        """ Generates alternate chords by just specifying a base combo

        Combos are implicitly distinct/unique and sorted on output.

        :param sizes: The sizes of the chords. e.g. ([1,2][3,4])
        :param keys: The keys of the map.
        :param method: Method to use, see PtnComboMethod. e.g. To use all methods:
            method=Method.ANY_ORDER | Method.AND_LOWER | Method.AND_HIGHER
        :param invertFilter: Whether to invert the filter, if True, these combos will be excluded
        :return:
        """
        sizes_ = np.array(sizes)
        if np.ndim(sizes_) < 2: cols_ = np.expand_dims(sizes, axis=list(range(2 - np.ndim(sizes_))))
        chunkSize = sizes_.shape[1]

        if method & PtnFilterChord.Method.AND_HIGHER == PtnFilterChord.Method.AND_HIGHER:
            sizesNew = np.array(np.meshgrid(*[list(range(i, keys + 1)) for i in np.min(sizes_, axis=0)]))\
                .T.reshape(-1, chunkSize)
            sizes_ = np.concatenate([sizes_, sizesNew], axis=0)

        if method & PtnFilterChord.Method.AND_LOWER == PtnFilterChord.Method.AND_LOWER:
            sizesNew = np.array(np.meshgrid(*[list(range(1, i + 1)) for i in np.max(sizes_, axis=0)]))\
                .T.reshape(-1, chunkSize)
            sizes_ = np.concatenate([sizes_, sizesNew], axis=0)

        if method & PtnFilterChord.Method.ANY_ORDER == PtnFilterChord.Method.ANY_ORDER:
            sizes_ = np.unique(np.array([list(permutations(i)) for i in sizes_]).reshape(-1, chunkSize), axis=0)

        return PtnFilterChord(sizes_, invertFilter)

