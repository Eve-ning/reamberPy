from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import List

import numpy as np


@dataclass
class PtnFilter:

    ar: np.ndarray
    keys: int = 0
    invertFilter: bool = False

    def __and__(self, other: PtnFilter or np.ndarray):
        """ This finds the intersects of these 2 arrays

        The method used here is pretty interesting.

        1. We firstly convert self and other to structured arrays, this operation gives each entry a temp name.
        2. We then used intersect1d. This works because each entry is now treated as one entity
        3. We then extract everything by doing a single-index extraction with the names.

        The catch for single vs. multi index is that if you do multi-index, you'll end up extracting a structured array.

        """
        self_ = np.asarray(np.core.records.fromarrays(self.ar.transpose()))
        other_ = np.asarray(np.core.records.fromarrays(other.ar.transpose() if isinstance(other, PtnFilter)
                                                                          else other.transpose().astype('<i4')))

        # noinspection PyTypeChecker
        new_ = np.intersect1d(self_, other_)
        return PtnFilter(np.asarray([new_[n] for n in self_.dtype.names]).transpose())

    def __or__(self, other: PtnFilter or np.ndarray):
        """ This finds the union of these 2 arrays """

        # This is much easier to write :)
        return PtnFilter(np.unique(
            np.concatenate([self.ar, other.ar if isinstance(other, PtnFilter) else other.astype('<i4')], axis=0),
            axis=0))

    def filter(self, data): ...

class PtnFilterCombo(PtnFilter):
    """ This class helps generate a lambda fitting for passing it into combinations. """

    def filter(self, data: np.ndarray) -> np.ndarray:
        # [[0 1 2], [0 1 3]]

        seq_size = data.shape[1]
        data_ = np.sum(data * self.keys ** np.arange(seq_size - 1, -1, -1), axis=1)
        self_ = np.sum(self.ar * self.keys ** np.arange(seq_size - 1, -1, -1), axis=1)
        return np.invert(np.isin(data_, self_)) if self.invertFilter else np.isin(data_, self_)

    class Method:
        """ The methods available to use in fromCombo
        
        Repeat just repeats the base pattern without changing its orientation.
        
        ``[0][1] --REPEAT-> [[0][1],[1][2],[2][3]]`` for keys=4
        
        Hmirror reflects the pattern on the y-axis
        
        ``[0][1] --HMIRROR-> [[0][1],[2][3]]`` for keys=4
        
        Vmirror reflects the pattern on the x-axis
        
        ``[0][1] --HMIRROR-> [[0][1],[1][0]]``
        
        """
        REPEAT: int = 2 ** 0
        HMIRROR: int = 2 ** 1
        VMIRROR: int = 2 ** 2

    @staticmethod
    def create(cols: List[List[int]],
               keys: int,
               method: Method or int = 0,
               invert_filter: bool = False) -> PtnFilterCombo:
        """ Generates alternate combos by just specifying a base combo
        
        Combos are implicitly distinct/unique and sorted on output.

        :param cols: The cols of the combo. e.g. ([1,2][3,4])
        :param keys: The keys of the map.
        :param method: Method to use, see PtnFilterCombo.Method
        :param invert_filter: Whether to invert the filter, if True, these combos will be excluded
        :return:
        """
        cols_ = np.asarray(cols) if isinstance(cols, List) else cols
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

        return PtnFilterCombo(ar=np.unique(cols_, axis=0), keys=keys, invertFilter=invert_filter)


class PtnFilterChord(PtnFilter):
    """ This class helps generate a lambda fitting for passing it into combinations. """

    def filter(self, data: np.ndarray) -> bool:
        seqSize = data.shape[0]
        data_ = np.sum(data * self.keys ** np.arange(seqSize - 1, -1, -1), axis=0)
        self_ = np.sum(self.ar * self.keys ** np.arange(seqSize - 1, -1, -1), axis=1)

        return not bool(np.isin(data_, self_)) if self.invertFilter else bool(np.isin(data_, self_))

    class Method:
        """ The methods available to use in fromChord

        AnyOrder generates any chord sequences that is a combination of the current

        ``[2][2][1] --ANYORDER-> [[2][2][1],[1][2][2],[2][1][2]]``

        AndLower generates any chord sequences that is lower than the current

        ``[2][2][1] --ANDLOWER-> [[2][2][1],[1][2][1],[2][1][1],[1][1][1]]``
        
        AndHigher is just the opposite of AndLower

        """
        ANY_ORDER: int = 2 ** 0
        AND_LOWER: int = 2 ** 1
        AND_HIGHER: int = 2 ** 2

    @staticmethod
    def create(sizes: List[List[int]], keys:int,
               method: PtnFilterChord.Method or int = 0,
               invert_filter:bool = False) -> PtnFilterChord:
        """ Generates alternate chords by just specifying a base combo

        Combos are implicitly distinct/unique and sorted on output.

        :param sizes: The sizes of the chords. e.g. ([1,2][3,4])
        :param keys: The keys of the map.
        :param method: Method to use, see PtnFilterChord.Method
        :param invert_filter: Whether to invert the filter, if True, these chords will be excluded
        :return:
        """
        sizes_ = np.asarray(sizes)
        if np.ndim(sizes_) < 2: sizes_ = np.expand_dims(sizes, axis=list(range(2 - np.ndim(sizes_))))
        chunk_size = sizes_.shape[1]

        if method & PtnFilterChord.Method.AND_HIGHER == PtnFilterChord.Method.AND_HIGHER:
            sizes_new = np.asarray(np.meshgrid(*[list(range(i, keys + 1)) for i in np.min(sizes_, axis=0)]))\
                .T.reshape(-1, chunk_size)
            sizes_ = np.concatenate([sizes_, sizes_new], axis=0)

        if method & PtnFilterChord.Method.AND_LOWER == PtnFilterChord.Method.AND_LOWER:
            sizes_new = np.asarray(np.meshgrid(*[list(range(1, i + 1)) for i in np.max(sizes_, axis=0)]))\
                .T.reshape(-1, chunk_size)
            sizes_ = np.concatenate([sizes_, sizes_new], axis=0)

        if method & PtnFilterChord.Method.ANY_ORDER == PtnFilterChord.Method.ANY_ORDER:
            sizes_ = np.unique(np.asarray([list(permutations(i)) for i in sizes_]).reshape(-1, chunk_size), axis=0)

        return PtnFilterChord(ar=sizes_, keys=keys, invertFilter=invert_filter)


class PtnFilterType(PtnFilter):
    """ This class helps generate a lambda fitting for passing it into combinations. """

    def filter(self, data: np.ndarray) -> np.ndarray:
        logic = np.zeros(data.shape[0], dtype=bool)

        for i, o in enumerate(data):
            for s in self.ar:
                if np.alltrue([issubclass(i, j) for i, j in zip(o, s)]):
                    logic[i] = True
                    break

        return np.invert(logic) if self.invertFilter else logic

    class Method:
        """ The methods available to use in fromChord

        AnyOrder generates any chord sequences that is a combination of the current

        ``[A][A][B] --ANYORDER-> [[A][A][B],[A][B][A],[B][A][A]]``

        mirror generates a flipped copy

        ``[A][A][B] --VMIRROR-> [[A][A][B],[B][A][A]]``

        """
        ANY_ORDER: int = 2 ** 0
        MIRROR: int = 2 ** 1

    @staticmethod
    def create(types: List[List[type]],
               keys: int,
               method: PtnFilterType.Method or int = 0,
               invert_filter: bool = False) -> PtnFilterType:
        """ Generates alternate chords by just specifying a base combo

        Combos are implicitly distinct/unique and sorted on output.

        :param types: The types of the sequence. e.g. [[A,B][B,A]]
        :param keys: The keys of the map
        :param method: Method to use, see PtnFilterClass.Method
        :param invert_filter: Whether to invert the filter, if True, these types will be excluded
        :return:
        """
        types_ = np.asarray(types)
        if np.ndim(types_) < 2: types_ = np.expand_dims(types_, axis=list(range(2 - np.ndim(types_))))
        chunk_size = types_.shape[1]

        if method & PtnFilterType.Method.ANY_ORDER == PtnFilterType.Method.ANY_ORDER:
            types_ = np.asarray([list(permutations(i)) for i in types_]).reshape(-1, chunk_size)

        elif method & PtnFilterType.Method.MIRROR == PtnFilterType.Method.MIRROR:
            types_ = np.concatenate([types_, np.flip(types_, axis=[1])])

        return PtnFilterType(ar=types_, keys=keys, invertFilter=invert_filter)
