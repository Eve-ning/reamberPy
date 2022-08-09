from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, List

import numpy as np

if TYPE_CHECKING:
    from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterType, \
    PtnFilterCombo
from reamber.base.Hold import HoldTail


class _PtnCJack:
    """Fragment of PtnCombo"""

    @abstractmethod
    def combinations(self, *args, **kwargs): ...

    def template_jacks(self: 'PtnCombo',
                       minimum_length: int,
                       keys: int) -> List[np.ndarray]:
        """A template to quickly create jack lines

        Notes:
            E.g. If the ``minimumLength==2``,
            all jacks that last at least 2 notes are highlighted.

        Args:
            minimum_length: The minimum length of the jack
            keys: The keys of the map, used to detect pattern limits.
        """

        if minimum_length < 2:
            raise ValueError(f"Min Length must be >= 2, {minimum_length} < 2")

        return self.combinations(
            size=minimum_length,
            make_size2=True,
            combo_filter=PtnFilterCombo.create(
                [[0] * minimum_length], keys=keys,
                options=PtnFilterCombo.Option.REPEAT,
                exclude=False).filter,
            type_filter=PtnFilterType.create(
                [[HoldTail] + [object, ] * (minimum_length - 1)],
                options=PtnFilterType.Option.ANY_ORDER,
                exclude=True).filter
        )
