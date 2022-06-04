""" A Scroll Velocity Sequence is a 'property' class, where it holds information on how a SV should
be created.

More information and traits can be added onto this Class inside the parts package within this directory
"""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import List, overload, Tuple

import numpy as np

from reamber.algorithms.generate.sv.SvIO import SvIO
from reamber.algorithms.generate.sv.SvObj import SvObj
from reamber.base.Property import list_props
from reamber.base.lists.TimedList import TimedList

log = logging.getLogger(__name__)


@list_props(SvObj)
class SvSequence(TimedList[SvObj], SvIO):

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
        raise DeprecationWarning("SV Sequencing is not available in this version. It'll be restored soon.")
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
        first_self, lastSelf = self.first_last_offset()
        duration_self = lastSelf - first_self
        duration_scale = last_offset - first_offset

        this = self if inplace else self.deepcopy()
        this.offsets -= first_self
        this.offsets *= duration_scale / duration_self
        this.offsets += first_offset

        return None if inplace else this

    def normalize_to(self,
                     ave_sv: float = 1.0,
                     inplace: bool = False,
                     ignore_fixed: bool = False,
                     min_allowable: float = None,
                     max_allowable: float = None,
                     scale_end: bool = True) -> SvSequence or None:
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

        :param ave_sv: The SV to average to.
        :param inplace: Whether to perform the operation inplace or not.
        :param ignore_fixed: Whether to ignore the fixed trait and just scale everything.
        :param min_allowable: Minimum allowable SV. Raises AssertionError on failure
        :param max_allowable: Maximum allowable SV. Raises AssertionError on failure
        :param scale_end: Whether to make the end Sv == aveSv
        """

        # Firstly, we find out if it's possible to normalize
        # Last Offset is implicitly the last Sv, which is ignored anyways.
        # TODO: Verify that the new activity works.
        acts: np.ndarray = self.time_diff()

        fixed_area: float = 0.0
        loose_area: float = 0.0

        first, last = self.first_last_offset()
        expected_area = (last - first) * ave_sv

        # Loop through the activities and find the total areas
        for obj, act in zip(self.df.iterrows(), acts):
            if obj.fixed and not ignore_fixed:  # Check if fixed is ignored also
                fixed_area += obj.multiplier * act
            else:
                loose_area += obj.multiplier * act

        required_scale = (expected_area - fixed_area) / loose_area

        log.debug(f"Fixed Area: {fixed_area}")
        log.debug(f"Loose Area: {loose_area}")
        log.debug(f"Expected Area: {expected_area}")
        log.debug(f"Required Loose Scaling: {required_scale}")

        norm_svs: List[SvObj] = []

        # Scale all loose Svs
        for act in acts[:-1]:
            if act[0].fixed and not ignore_fixed:  # Check if fixed is ignored also
                norm_svs.append(act[0])
            else:
                sv = act[0]
                sv.multiplier *= required_scale

                # Assert allowable
                if min_allowable is not None:
                    assert sv.multiplier >= min_allowable, f"Sv Multiplier {sv.multiplier} < Allowable {min_allowable}"
                if max_allowable is not None:
                    assert sv.multiplier <= max_allowable, f"Sv Multiplier {sv.multiplier} > Allowable {max_allowable}"
                norm_svs.append(sv)

        # Append last Sv
        if scale_end:
            end_sv = acts[-1][0]
            end_sv.multiplier = ave_sv
            norm_svs.append(end_sv)
        else:
            norm_svs.append(acts[-1][0])

        if inplace: self.__init__(norm_svs)
        else: return SvSequence(norm_svs)

    @overload
    def append_init(self, list_: List[SvObj]): ...
    @overload
    def append_init(self, list_: List[Tuple[float, float, bool]]): ...
    @overload
    def append_init(self, list_: List[Tuple[float, float]]): ...
    @overload
    def append_init(self, list_: List[float]): ...
    def append_init(self, list_: List):
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

    def cross_with(self, other: SvSequence, inplace: bool = False):
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
        this_i = 0
        other_i = 0
        this = self if inplace else self.deepcopy()
        this = this.sorted()
        other_ = other.sorted()
        while True:
            if this_i == len(this): break
            this_sv = this[this_i]
            other_sv = other_[other_i]
            multiplier = other_sv.multiplier
            other_next_sv = None if other_i == len(other_) - 1 else other_[other_i + 1]
            if this_sv.offset < other_sv.offset:
                this_i += 1
                continue
            if other_next_sv is not None and this_sv.offset >= other_next_sv.offset:
                other_i += 1
                continue
            this_sv.multiplier *= multiplier
            this_i += 1

        return None if inplace else this

    def multiply_mul(self, by: float, inplace: bool = False):
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
    def add_mul(self, by: float, inplace: bool = False):
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

