from __future__ import annotations
from typing import List
from reamber.base.Hold import HoldTail
from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterType, PtnFilterCombo
from reamber.algorithms.pattern.combos.PtnCombo import PtnCombo
import numpy as np


class PtnCJack:
    """ Fragment of PtnCombo """

    @staticmethod
    def templateJacks(minimumLength: int,
                      keys:int, groups: List[np.ndarray]) -> np.ndarray:
        """ A template to quickly create jack lines

        E.g. If the ``minimumLength==2``, all jacks that last at least 2 notes are highlighted.

        :param minimumLength: The minimum length of the jack
        :param keys: The keys of the map, used to detect pattern limits.
        :param groups: The grouping of the notes, generated from Pattern.grp
        :return:
        """

        assert minimumLength >= 2, f"Minimum Length must be at least 2, {minimumLength} < 2"
        combo = PtnCombo.combinations(
            groups,
            size=minimumLength,
            flatten=True,
            makeSize2=True,
            comboFilter=PtnFilterCombo.create(
                [[0] * minimumLength], keys=keys,
                method=PtnFilterCombo.Method.REPEAT,
                invertFilter=False).filter,
            typeFilter=PtnFilterType.create(
                [[HoldTail, object]],
                method=PtnFilterType.Method.ANY_ORDER,
                invertFilter=True).filter)

        return combo
