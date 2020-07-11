from __future__ import annotations
from typing import List
from reamber.base.Hold import HoldTail
from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterType, PtnFilterCombo
import numpy as np
from abc import abstractmethod


class _PtnCJack:
    """ Fragment of PtnCombo """

    @abstractmethod
    def combinations(self, *args, **kwargs): ...

    def templateJacks(self, minimumLength: int,
                      keys:int) -> np.ndarray:
        """ A template to quickly create jack lines

        E.g. If the ``minimumLength==2``, all jacks that last at least 2 notes are highlighted.

        :param minimumLength: The minimum length of the jack
        :param keys: The keys of the map, used to detect pattern limits.
        :return:
        """

        assert minimumLength >= 2, f"Minimum Length must be at least 2, {minimumLength} < 2"
        # noinspection PyTypeChecker
        return self.combinations(
            size=minimumLength,
            flatten=True,
            makeSize2=True,
            comboFilter=PtnFilterCombo.create(
                [[0] * minimumLength], keys=keys,
                method=PtnFilterCombo.Method.REPEAT,
                invertFilter=False).filter,
            typeFilter=PtnFilterType.create(
                [[HoldTail] + [object] * (minimumLength - 1)], keys=keys,
                method=PtnFilterType.Method.ANY_ORDER,
                invertFilter=True).filter)
