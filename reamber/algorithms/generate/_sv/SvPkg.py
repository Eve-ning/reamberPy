from __future__ import annotations

from enum import Enum
from typing import List, Callable

from numpy import linspace

from reamber.algorithms.generate.sv.SvSequence import SvSequence


class SvPkg(List[SvSequence]):

    def __init__(self, list_):
        list.__init__(self, list_)

    class CombineMethod(Enum):
        """ Specifies the combine methods

        - **IGNORE**: Ignores repeated Svs
        - **DROP_BY_POINT**: Drops pts within window ms of each other
        - **DROP_BY_BOUND**: Drops pts earlier than the previous list's end.

        Example::

            LIST 1    |[1     1     1]      |
            LIST 2    |   [2  2  2  2  2  2]|
            IGNORE    | 1  2 1&2 2 1&2 2  2 | All combo optimizations ignored.
            D_B_POINT |[1 [2  1  2  1] 2  2]| Note: bounds overlap.
            D_B_BOUND |[1     1     1][2  2]| Note: bounds don't overlap.

        """

        IGNORE = 0
        DROP_BY_POINT = 1
        DROP_BY_BOUND = 2

    def apply_nth(self,
                  func: Callable[[float], float] | List[float] | float,
                  nth: int,
                  start_x: float = 0,
                  end_x: float = 1) -> None:
        """ Applies the function to the nth element's multiplier of
         every sequence. Always inplace.

        Example::

            If start_x = 0, end_x = 1.
            The function will go from 0 to 1 within the sequences linearly.

            If a Callable is passed, if there are 11 sequences,
             it'll call func(0), func(0.1), ..., func(1).

        Args:
            func: A function / list of multiplier / constant to apply
            nth: The nth element to apply to
            start_x: The start X
            end_x: The end X
        """

        if isinstance(func, (float, int)):
            func = [func for _ in range(len(self))]
        elif isinstance(func, Callable):
            func = [func(x) for x in list(linspace(start_x, end_x, len(self)))]

        assert len(func) == len(self), "Lengths must match."
        assert nth < len(self[0]), "nth must be within the list index"

        for mul, seq in zip(func, self):
            seq[nth].multiplier = mul

    def combine(self,
                combine_method: CombineMethod = CombineMethod.IGNORE,
                combine_method_window: float = 1.0,
                combine_priority_last: bool = True) -> SvSequence:

        """ Combines multiple sequences together

        See Also:
            SvSequence.CombineMethod

        Args:
            combine_method: Method to use for combination.
            combine_method_window: ms window to check if offsets are same offset.
                Can be 0 for exact comparison
            combine_priority_last: If True, this means that the later SVs will
             overlap the earlier ones. Recommended for current API
        """

        if combine_method == self.CombineMethod.IGNORE:
            return sorted(SvSequence([x for y in self for x in y]))
        elif combine_method == self.CombineMethod.DROP_BY_POINT:
            new_seq = sorted(SvSequence([x for y in self for x in y]))
            if combine_priority_last: new_seq.reverse()
            # If the next offset is similar to current, we delete the next one
            # else we move to the next element
            i = 0
            while i < len(new_seq) - 1:
                if new_seq[i + 1].offset - combine_method_window <= \
                    new_seq[i].offset <= \
                    new_seq[i + 1].offset + combine_method_window:
                    del new_seq[i + 1]
                else:
                    i += 1

            return sorted(new_seq) if combine_priority_last else new_seq
        else:  # Combine Method == DROP_BY_BOUND
            new_seq = self[0].sorted()
            if combine_priority_last: new_seq.reverse()
            seq_end = new_seq.last_offset()
            for seq in self[1:]:
                add_seq = seq.after(offset=seq_end, include_end=False,
                                    inplace=False)
                new_seq += add_seq
                seq_end = add_seq.last_offset()
            return new_seq.sorted() if combine_priority_last else new_seq

    def add_offset(self, by: float):
        this = self.deepcopy(self)
        for i in this: i.offsets += by
        return this

    def mult_offset(self, by: float):
        this = self.deepcopy(self)
        for i in this: i.offsets *= by
        return this

    @staticmethod
    def fit(seq: SvSequence, offsets: List[float]) -> SvPkg:
        """ Repeats the Sequence such that it repeats from offset to offset,
        scaled correctly. Always sorts offsets

        Example::

            Input Sequence
            OFFSETS 100 150 200
            SEQ     1.5 0.5 1.0

            Input Offsets
            OFFSETS 100 200 300     500     700

            Output
            SEQ 1        SEQ 2        SEQ 3        SEQ 4
            ---------------------------------------------------
            OFFSET SV  | OFFSET SV  | OFFSET SV  | OFFSET SV  |
            100    1.5 | 200    1.5 | 300    1.5 | 500    1.5 |
            150    0.5 | 250    0.5 | 400    0.5 | 600    0.5 |
            200    1.0 | 300    1.0 | 500    1.0 | 700    1.0 |

        Args:
            seq: The sequence to fit
            offsets: The offsets to fit to.
        """
        offsets_ = sorted(offsets)
        seqs = []
        for first_offset, last_offset in zip(offsets_[:-1], offsets_[1:]):
            seqs.append(seq.move_start_to(first_offset)
                        .rescale(first_offset, last_offset))

        return SvPkg(seqs)

    @staticmethod
    def repeat(seq: SvSequence, times: int, gap: float = 0) -> SvPkg:
        """ Repeats the Sequence by copying the sequence to the end.

        Always includes current sequence.

        Consider::

            <---> repeated 3 times.

            <--->
                <--->
                    <--->

        Args:
            seq: The SvSequence To Repeat
            times: Number of times to repeat
            gap: The gap between each repeat
        """
        first, last = seq.first_last_offset()
        duration = last - first
        return SvPkg.copy_to(
            seq=seq,
            offsets=[first + (duration + gap) * i for i in range(times)]
        )

    @staticmethod
    def copy_to(seq: SvSequence, offsets: List[float]) -> SvPkg:
        """ Copies self to specified offsets

        Args:
            seq: The SvSequence To Copy
            offsets: Offsets in float
        """
        pkg = []
        for offset in offsets:
            seq_ = seq.deepcopy()
            seq_.offsets += offset - seq.first_offset()
            pkg.append(seq_)
        return SvPkg(pkg)

    @staticmethod
    def cross_mutual_with(this: SvSequence, other: SvSequence) -> SvPkg:
        """ Crosses each other mutually """
        return SvPkg([this.cross_with(other=other, inplace=False),
                      other.cross_with(other=this, inplace=False)])
