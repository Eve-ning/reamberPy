from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations
from typing import List

import numpy as np


@dataclass
class PtnFilter:
    ar: np.ndarray
    keys: int = 0
    invert_filter: bool = False

    def __and__(self, other: PtnFilter or np.ndarray):
        """This finds the intersects of these 2 arrays

        1. We firstly convert self and other to structured arrays, this
            operation gives each entry a temp name.
        2. We then used intersect1d. This works because each entry is now
            treated as one entity
        3. We then extract everything by doing a single-index extraction with
            the names.

        The catch for single vs. multi index is that if you do multi-index,
            you'll end up extracting a structured array.

        """
        ar_self = np.asarray(
            np.core.records.fromarrays(self.ar.transpose())
        )
        ar_other = np.asarray(
            np.core.records.fromarrays(
                other.ar.transpose()
                if isinstance(other, PtnFilter)
                else other.transpose().astype('<i4')
            )
        )

        # noinspection PyTypeChecker
        new_ = np.intersect1d(ar_self, ar_other)
        return PtnFilter(
            np.asarray([new_[n] for n in ar_self.dtype.names]).transpose()
        )

    def __or__(self, other: PtnFilter or np.ndarray):
        """This finds the union of these 2 arrays"""

        return PtnFilter(np.unique(
            np.concatenate([
                self.ar,
                other.ar if isinstance(other, PtnFilter)
                else other.astype('<i4')
            ], axis=0),
            axis=0))

    def filter(self, data): ...


class PtnFilterCombo(PtnFilter):
    """This class helps generate a lambda fitting for combinations. """

    def filter(self, data: np.ndarray) -> np.ndarray:
        """Given a ndarray of (n, 2), it will return an n length boolean
         to accept

        This checks if data is in the self.ar filter.

        This is done by creating a unique hash of every combination then 
            comparing if they contain

        """

        seq_size = data.shape[1]
        data_ = np.sum(
            data * self.keys ** np.arange(seq_size - 1, -1, -1), axis=1
        )
        self_ = np.sum(
            self.ar * self.keys ** np.arange(seq_size - 1, -1, -1), axis=1
        )
        return (
            np.invert(np.isin(data_, self_))
            if self.invert_filter else np.isin(data_, self_)
        )

    class Option:
        """The methods available to use in fromCombo

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
    def create(combos: List[List[int]],
               keys: int,
               options: PtnFilterCombo.Option | int = 0,
               exclude: bool = False) -> PtnFilterCombo:
        """Generates alternate combos by just specifying a base combo
        
        Args:
            combos: The cols of the combo. e.g. ([1,2][3,4])
            keys: The keys of the map.
            options: Method to use, see PtnFilterCombo.Method
            exclude: Whether to invert the filter, if True, these combos will 
                be excluded
        """
        ar_combos = np.asarray(combos) if isinstance(combos, List) else combos
        if np.ndim(ar_combos) < 2:
            ar_combos = ar_combos[..., np.newaxis]

        Option = PtnFilterCombo.Option
        if options & Option.REPEAT == Option.REPEAT:

            """
            Keys    | _ _ 0 _ 0 _ _ |                
            Min     |     ^         |        
            Max     |         ^     |

            Freedom defines how much 1-step movement can the 
            pattern have without exceeding the limits

            E.g.
            | 0 _ _ 0 | has no freedom as +-1 will be out of bounds

            | 0 _ 0 _ | has freedom = 1 as we can shift it 1 right
            | _ 0 _ 0 | <- 1 Right

            | _ 0 0 _ | has freedom = 2 as we can shift it 1 right and 1 left
            | _ _ 0 0 | <- 1 Right
            | 0 0 _ _ | <- 1 Left

            | _ _ 0 _ | has freedom = 3 as we can shift it 1 right and 2 left
            | _ _ _ 0 | <- 1 Right
            | _ 0 _ _ | <- 1 Left
            | 0 _ _ _ | <- 2 Left

            Freedom Delta defines the list of possible shifts you can do while
            keeping it in bounds. 


            """

            ar_combo_repeats = []
            # E.g. [[1, 2]] in key = 4
            for e, ar_combo in enumerate(ar_combos):
                minimum = np.min(ar_combo)  # E.g. 1
                maximum = np.max(ar_combo)  # E.g. 2
                freedom = keys - maximum + minimum  # E.g. 2, 1L1R
                freedom_delta = np.arange(freedom) - minimum  # E.g. [-1, 0, 1]

                # E.g. [[0, 1], [1, 2], [2, 3]]
                ar_combo_repeats.append(
                    ar_combo + freedom_delta[..., np.newaxis])

            ar_combos = np.concatenate(ar_combo_repeats)

        if options & Option.HMIRROR:
            ar_combos = np.concatenate([ar_combos, (keys - 1) - ar_combos])

        if options & Option.VMIRROR:
            ar_combos = np.concatenate(
                [ar_combos, np.flip(ar_combos, axis=[1])])

        return PtnFilterCombo(ar=np.unique(ar_combos, axis=0), keys=keys,
                              invert_filter=exclude)


class PtnFilterChord(PtnFilter):
    """This class helps generate a lambda fitting for combinations. """

    def filter(self, data: np.ndarray) -> bool:
        """This simply checks if the data is contained in self.ar simply

        Returns:
            A boolean on filter result
        """

        return data not in self.ar if self.invert_filter else data in self.ar

    class Option:
        """The methods available to use in fromChord

        AnyOrder generates any chord sequences that is a combination of the
         current

        ``[2][2][1] --ANYORDER-> [[2][2][1],[1][2][2],[2][1][2]]``

        AndLower generates any chord sequences that is lower than the current

        ``[2][2][1] --ANDLOWER-> [[2][2][1],[1][2][1],[2][1][1],[1][1][1]]``
        
        AndHigher is just the opposite of AndLower

        """
        ANY_ORDER: int = 2 ** 0
        AND_LOWER: int = 2 ** 1
        AND_HIGHER: int = 2 ** 2

    @staticmethod
    def create(chord_sizes: List[List[int]], keys: int,
               options: PtnFilterChord.Option | int = 0,
               exclude: bool = False) -> PtnFilterChord:
        """Generates alternate chords by just specifying a base combo

        Args:
            chord_sizes: The sizes of the chords. e.g. ([1,2][3,4])
            keys: The keys of the map.
            options: Method to use, see PtnFilterChord.Method
            exclude: Whether to excluded
        """
        sizes_ = np.asarray(chord_sizes)
        if np.ndim(sizes_) < 2: sizes_ = \
            np.expand_dims(chord_sizes, axis=list(range(2 - np.ndim(sizes_))))
        chunk_size = sizes_.shape[1]

        Option = PtnFilterChord.Option
        if options & Option.AND_HIGHER:
            sizes_new = np.asarray(np.meshgrid(
                *[list(range(i, keys + 1)) for i in np.min(sizes_, axis=0)])) \
                .T.reshape(-1, chunk_size)
            sizes_ = np.concatenate([sizes_, sizes_new], axis=0)

        if options & Option.AND_LOWER:
            sizes_new = np.asarray(np.meshgrid(
                *[list(range(1, i + 1)) for i in np.max(sizes_, axis=0)])) \
                .T.reshape(-1, chunk_size)
            sizes_ = np.concatenate([sizes_, sizes_new], axis=0)

        if options & Option.ANY_ORDER:
            sizes_ = np.asarray([list(permutations(i)) for i in sizes_]) \
                .reshape(-1, chunk_size)

        return PtnFilterChord(ar=np.unique(sizes_, axis=0),
                              keys=keys, invert_filter=exclude)


class PtnFilterType(PtnFilter):
    """This class helps generate a lambda fitting for combinations. """

    def filter(self, data: np.ndarray) -> np.ndarray:
        """This loops and checks if data are a subclass of what's filtering

        Returns:
            An n length boolean on filter result
        """
        logic = np.zeros(data.shape[0], dtype=bool)

        if data.size == 0: return logic

        for type_filter in self.ar:
            filter_result = []
            for ix, cls in enumerate(type_filter):
                filter_result.append(
                    np.vectorize(lambda x: issubclass(x, cls))(data[:, ix]))

            logic |= np.all(np.asarray(filter_result), axis=0)
        return np.invert(logic) if self.invert_filter else logic

    class Option:
        """The methods available to use in fromChord

        ANY_ORDER generates any chord sequences that is a combination of the
            current

        ``[A][A][B] --ANY_ORDER-> [[A][A][B],[A][B][A],[B][A][A]]``

        MIRROR generates a flipped copy

        ``[A][A][B] --VMIRROR-> [[A][A][B],[B][A][A]]``

        """
        ANY_ORDER: int = 2 ** 0
        MIRROR: int = 2 ** 1

    @staticmethod
    def create(types: List[List[type]],
               options: PtnFilterType.Option or int = 0,
               exclude: bool = False) -> PtnFilterType:
        """Generates alternate chords by just specifying a base combo

        Args:
            types: The types of the sequence. e.g. [[A,B], [B,A]]
            options: Method to use, see PtnFilterClass.Method
            exclude: Whether to invert the filter, if True,
                these types will be excluded
        """
        types_ = np.asarray(types)
        if np.ndim(types_) < 2:
            types_ = types_[..., np.newaxis]
        chunk_size = types_.shape[1]

        Option = PtnFilterType.Option
        if options & Option.ANY_ORDER:
            types_ = np.asarray(
                [list(permutations(i)) for i in types_]
            ).reshape(-1, chunk_size)

        elif options & Option.MIRROR:
            types_ = np.concatenate([types_, np.flip(types_, axis=[1])])

        _, unq_ix = np.unique(list(map(str, types_)), return_index=True)
        return PtnFilterType(ar=types_[unq_ix],
                             keys=0, invert_filter=exclude)
