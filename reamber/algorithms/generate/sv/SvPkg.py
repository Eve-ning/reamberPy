from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from reamber.algorithms.generate.sv.SvSequence import SvSequence
from enum import Enum

@dataclass
class SvPkg:
    seqs: List[SvSequence] = field(default_factory=lambda: [])

    class CombineMethod(Enum):
        """ Specifies the combine methods

        IGNORE: Ignores repeated Svs
        DROP_BY_POINT: Drops points that are within window ms of each other
        DROP_BY_BOUND: Drops points that are earlier than the previous list's end.

        Example::

            LIST 1    |[1     1     1]      |
            LIST 2    |   [2  2  2  2  2  2]|
            IGNORE    | 1  2 1&2 2 1&2 2  2 | All combination optimizations are ignored.
            D_B_POINT |[1 [2  1  2  1] 2  2]| Note that the bounds overlap.
            D_B_BOUND |[1     1     1][2  2]| Note that the bounds don't overlap.

        """

        IGNORE = 0
        DROP_BY_POINT = 1
        DROP_BY_BOUND = 2

    def combine(self, combineMethod: CombineMethod = CombineMethod.IGNORE,
                combineMethodWindow: float = 1.0,
                combinePriorityLast: bool = True) -> SvSequence:

        """ Combines multiple sequences together

        Can specify to keep earliest SV if overlapping.

        :param combineMethod: The method to use to combine. See SvSequence.CombineMethod
        :param combineMethodWindow: The millisecond window to check if offsets are of the same offset. Can be 0 for\
            exact comparison
        :param combinePriorityLast: If True, this means that the later SVs will overlap the earlier ones. Recommended\
            for current API
        :return: Returns a stable sorted combine
        """

        if combineMethod == self.CombineMethod.IGNORE:
            return SvSequence([x for y in self.seqs for x in y]).sorted(inplace=False)
        elif combineMethod == self.CombineMethod.DROP_BY_POINT:
            newSeq = SvSequence([x for y in self.seqs for x in y]).sorted(inplace=False)
            if combinePriorityLast: newSeq.reverse()
            # We loop through the list, if the next offset is similar to current, we delete the next one
            # else we move to the next element
            i = 0
            while i < len(newSeq) - 1:
                if newSeq[i + 1].offset - combineMethodWindow <= newSeq[i].offset <= \
                        newSeq[i + 1].offset + combineMethodWindow:
                    del newSeq[i + 1]
                else:
                    i += 1

            return newSeq.sorted() if combinePriorityLast else newSeq
        else:  # Combine Method == DROP_BY_BOUND
            newSeq = self.seqs[0].sorted()
            if combinePriorityLast: newSeq.reverse()
            seqEnd = newSeq.lastOffset()
            for seq in self.seqs[1:]:
                addSeq = seq.after(offset=seqEnd, includeEnd=False, inplace=False)
                newSeq += addSeq
                seqEnd = addSeq.lastOffset()
            return newSeq.sorted() if combinePriorityLast else newSeq

    @staticmethod
    def fit(seq: SvSequence, offsets: List[float]) -> SvPkg:
        """ Repeats the Sequence such that it repeats from offset to offset, scaled correctly. Always sorts offsets

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

        :param seq: The sequence to fit
        :param offsets: The offsets to fit to.
        """
        offsets_ = sorted(offsets)
        seqs = []
        for firstOffset, lastOffset in zip(offsets_[:-1], offsets_[1:]):
            seqs.append(seq.moveStartTo(firstOffset, inplace=False).rescale(firstOffset, lastOffset))

        return SvPkg(seqs=seqs)

    @staticmethod
    def repeat(seq: SvSequence, times: int, gap: float = 0) -> SvPkg:
        """ Repeats the Sequence by copying the the sequence to the end.

        Always includes current sequence.

        Consider::

            <---> repeated 2 times.

            <--->
                <--->
                    <--->

        :param seq: The SvSequence To Repeat
        :param times: Number of times to repeat
        :param gap: The gap between each repeat
        """
        first, last = seq.firstLastOffset()
        duration = last - first
        return SvPkg.copyTo(seq=seq, offsets=[first + (duration + gap) * i for i in range(times)])

    @staticmethod
    def copyTo(seq: SvSequence, offsets: List[float]) -> SvPkg:
        """ Copies self to specified offsets

        :param seq: The SvSequence To Copy
        :param offsets: Offsets in float
        :return: Returns a List of SvSequences, flatten-able by SvSequence.combine()
        """
        return SvPkg([seq.deepcopy().addOffset(offset - seq.firstOffset()) for offset in offsets])

    @staticmethod
    def crossMutualWith(this: SvSequence, other: SvSequence) -> SvPkg:
        """ Crosses with each other, returning 2 sequences that can be combined with SvPkg. """
        return SvPkg([this.crossWith(other=other, inplace=False),
                      other.crossWith(other=this, inplace=False)])
