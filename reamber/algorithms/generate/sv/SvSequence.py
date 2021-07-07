""" A Scroll Velocity Sequence is a 'property' class, where it holds information on how a SV should
be created.

More information and traits can be added onto this Class inside the parts package within this directory
"""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import List, overload, Tuple

from reamber.algorithms.generate.sv.SvIO import SvIO
from reamber.algorithms.generate.sv.SvObj import SvObj
from reamber.base.lists.TimedList import TimedList

log = logging.getLogger(__name__)


class SvSequence(List[SvObj], TimedList, SvIO):

    def _upcast(self, obj_list: List = None):
        return SvSequence(obj_list)
    def data(self) -> List[SvObj]:
        return self
    def deepcopy(self) -> SvSequence:
        return deepcopy(self)

    @overload
    def __init__(self, list_: List[SvObj] = None): ...
    @overload
    def __init__(self, list_: List[Tuple[float, float, bool]] = None): ...
    @overload
    def __init__(self, list_: List[Tuple[float, float]] = None): ...
    @overload
    def __init__(self, list_: List[float] = None): ...
    def __init__(self, list_: List = None):
        """ Multiple ways to initialize the sequence

        1. `SvSequence([Sv, Sv, ...])`
        2. `SvSequence([(offset, sv, fix), (offset, sv, fix), ...])`
        3. `SvSequence([(offset, sv), (offset, sv), ...])`
        4. `SvSequence([offset, offset, ...])`

        These also can be mixed.

        5. `SvSequence([Sv, (offset, sv), offset, ...])`
        """

        if list_ is not None:
            for i in range(len(list_)):
                item = list_[i]
                if isinstance(item, Tuple):
                    if len(item) == 2:
                        list_[i] = SvObj(offset=item[0], multiplier=item[1])
                    elif len(item) == 3:
                        list_[i] = SvObj(offset=item[0], multiplier=item[1], fixed=item[2])
                elif isinstance(item, float) or isinstance(item, int):
                    list_[i] = SvObj(offset=item)
                elif not isinstance(item, SvObj):
                    raise TypeError(f"Unexpected Type in list. {item}")

            list.__init__(self, list_)
        else:
            list.__init__(self, [])

    def rescale(self, first_offset: float, last_offset: float, inplace: bool = False) -> SvSequence or None:
        """ Scales the sequence to fit the sequence """
        firstSelf, lastSelf = self.first_last_offset()
        durationSelf = lastSelf - firstSelf
        durationScale = last_offset - first_offset

        this = self if inplace else self.deepcopy()
        this.add_offset(-firstSelf)
        this.mult_offset(durationScale / durationSelf)
        this.add_offset(first_offset)

        return None if inplace else this

    def normalizeTo(self,
                    aveSv: float = 1.0,
                    inplace: bool = False,
                    ignoreFixed: bool = False,
                    minAllowable: float = None,
                    maxAllowable: float = None,
                    scaleEnd: bool = True) -> SvSequence or None:
        """ Attempts to normalize the whole sequence to a specified average Sv.

        This also respects the fixed Sv concept::

            SVS   1.0 1.5 1.0
            FIXED     [F]
            -----------------
            Normalize to 1.0
            Last SV is ignored
            Hence, We adjust [0:-1]
            However [1] is fixed, so [0] is adjusted.
            -----------------------------------------
            SVS   0.5 1.5 1.0
            FIXED     [F]

        :param aveSv: The SV to average to.
        :param inplace: Whether to perform the operation inplace or not.
        :param ignoreFixed: Whether to ignore the fixed trait and just scale everything.
        :param minAllowable: Minimum allowable SV. Raises AssertionError on failure
        :param maxAllowable: Maximum allowable SV. Raises AssertionError on failure
        :param scaleEnd: Whether to make the end Sv == aveSv
        """

        # Firstly, we find out if it's possible to normalize
        # Last Offset is implicitly the last Sv, which is ignored anyways.
        # noinspection PyTypeChecker
        acts: List[Tuple[SvObj, float]] = self.activity()

        fixedArea: float = 0.0
        looseArea: float = 0.0

        first, last = self.first_last_offset()
        expectedArea = (last - first) * aveSv

        # Loop through the activities and find the total areas
        for act in acts:
            act: Tuple[SvObj, float]
            if act[0].fixed and not ignoreFixed:  # Check if fixed is ignored also
                fixedArea += act[0].multiplier * act[1]
            else:
                looseArea += act[0].multiplier * act[1]

        requiredScale = (expectedArea - fixedArea) / looseArea

        log.debug(f"Fixed Area: {fixedArea}")
        log.debug(f"Loose Area: {looseArea}")
        log.debug(f"Expected Area: {expectedArea}")
        log.debug(f"Required Loose Scaling: {requiredScale}")

        normSvs: List[SvObj] = []

        # Scale all loose Svs
        for act in acts[:-1]:
            if act[0].fixed and not ignoreFixed:  # Check if fixed is ignored also
                normSvs.append(act[0])
            else:
                sv = act[0]
                sv.multiplier *= requiredScale

                # Assert allowable
                if minAllowable is not None:
                    assert sv.multiplier >= minAllowable, f"Sv Multiplier {sv.multiplier} < Allowable {minAllowable}"
                if maxAllowable is not None:
                    assert sv.multiplier <= maxAllowable, f"Sv Multiplier {sv.multiplier} > Allowable {maxAllowable}"
                normSvs.append(sv)

        # Append last Sv
        if scaleEnd:
            endSv = acts[-1][0]
            endSv.multiplier = aveSv
            normSvs.append(endSv)
        else:
            normSvs.append(acts[-1][0])

        if inplace: self.__init__(normSvs)
        else: return SvSequence(normSvs)

    @overload
    def appendInit(self, list_: List[SvObj]): ...
    @overload
    def appendInit(self, list_: List[Tuple[float, float, bool]]): ...
    @overload
    def appendInit(self, list_: List[Tuple[float, float]]): ...
    @overload
    def appendInit(self, list_: List[float]): ...
    def appendInit(self, list_: List):
        """ Similar to initializing, we can append with multiple ways

        1. `append([SvObj, SvObj, ...])`
        2. `append([(offset, sv), (offset, sv), ...])`
        3. `append([offset, offset, ...])`

        These also can be mixed.

        4. `append([SvObj, (offset, sv), offset, ...])`
        """
        for i in range(len(list_)):
            item = list_[i]
            if isinstance(item, Tuple):
                if len(item) == 2:
                    list_[i] = SvObj(offset=item[0], multiplier=item[1])
                elif len(item) == 3:
                    list_[i] = SvObj(offset=item[0], multiplier=item[1], fixed=item[2])
            elif isinstance(item, float) or isinstance(item, int):
                list_[i] = SvObj(offset=item)
            elif not isinstance(item, SvObj):
                raise TypeError(f"Unexpected Type in list. {item}")

        self.extend(list_)

    def crossWith(self, other: SvSequence, inplace: bool = False):
        """ Cross Multiplies Sequences with each other. Will implicitly sort.

        Consider if you want to have a stutter that slows down, you'd need 2 sequences.

        1. A Slowdown Sequence
        2. A Stutter Sequence

        By crossing them together correctly, you'll achieve a slowdown stutter.

        If you want to keep the Sv Sequence of the stutter only, use `stutter.crossWith(slowdown)`.
        Vice versa.

        If you want to keep everything, including the slowdown during stutter, use fullCrossWith from SvPkg

        For Example::

            self Input         | (1.0) ------- (2.0) ------- (3.0) |
            other Input        | (1.0)  (1.5) ------- (2.0) ------ |
            __________________ | _________________________________ |
            fullCross == False | (1.0) ------- (3.0) ------- (6.0) |
            Not returned       | (1.0)  (1.5) ------- (4.0) ------ |
            fullCross == True  | (1.0)  (1.5)  (3.0)  (4.0)  (6.0) |

        :param other: The Sequence to cross against. Modifies current Sequence
        :param inplace: Whether to perform the operation inplace or not. Affects current Sequence only
        """
        thisI = 0
        otherI = 0
        this = self if inplace else self.deepcopy()
        this.sorted(inplace=True)
        other_ = other.sorted()
        while True:
            if thisI == len(this): break
            thisSv = this[thisI]
            otherSv = other_[otherI]
            multiplier = otherSv.multiplier
            otherNextSv = None if otherI == len(other_) - 1 else other_[otherI + 1]
            if thisSv.offset < otherSv.offset:
                thisI += 1
                continue
            if otherNextSv is not None and thisSv.offset >= otherNextSv.offset:
                otherI += 1
                continue
            thisSv.multiplier *= multiplier
            thisI += 1

        return None if inplace else this

    def multiplyMul(self, by: float, inplace: bool = False):
        """ Multiplies the whole sequence multiplier by

        :param by: The multiplication
        :param inplace: Whether to perform the operation inplace or not
        """
        if inplace:
            for i in self: i.multiplier *= by
        else:
            this = self.deepcopy()
            for i in this: i.multiplier *= by
            return this
    def addMul(self, by: float, inplace: bool = False):
        """ Multiplies the whole sequence multiplier by

        :param by: The addition
        :param inplace: Whether to perform the operation inplace or not
        """
        if inplace:
            for i in self: i.multiplier += by
        else:
            this = self.deepcopy()
            for i in this: i.multiplier += by
            return this

    def __str__(self) -> str:
        return "\n".join(["OFFSET    MULT           FIXED"]
                         + [f"{round(sv.offset,4):<10}"
                            f"{round(sv.multiplier,4):<15}"
                            f"{str(sv.fixed):<7}" for sv in self])

