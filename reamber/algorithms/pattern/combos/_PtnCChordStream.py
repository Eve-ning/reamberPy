from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, List

import numpy as np

from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterType, \
    PtnFilterCombo, PtnFilterChord
from reamber.base.Hold import HoldTail

if TYPE_CHECKING:
    from reamber.algorithms.pattern.combos import PtnCombo


class _PtnCChordStream:
    """Fragment of PtnCombo"""

    @abstractmethod
    def combinations(self, *args, **kwargs): ...

    def template_chord_stream(self: 'PtnCombo',
                              primary: int, secondary: int,
                              keys: int,
                              and_lower: bool = False,
                              include_jack: bool = False) -> List[np.ndarray]:
        """A template for chordstream filtering

        Notes:
            Primary & Secondary are the size of each chord.
            Jacks are automatically excluded unless specified.

            All chord sizes below it are also included if ``andBelow is True``

        Examples:
            a Jumpstream has ``primary=2, secondary=1``

            a Handstream detection can use
            - ``primary=3, secondary=2, and_lower=True``.

            and_lower implies accepting
            - ``primary=2, secondary=2``
            - ``primary=2, secondary=1``,
            - ``primary=1, secondary=1``.

        Args:
            primary: The primary chord size for each chord stream.
            secondary: The secondary chord size for each chord stream.
            keys: The keys of the map, used to detect pattern limits.
            and_lower: Whether to include lower size chords or not
            include_jack: Whether to include jackstreams or not
        """

        return self.combinations(
            size=2,
            make_size2=True,
            chord_filter=PtnFilterChord.create(
                [[primary, secondary]], keys=keys,
                options=PtnFilterChord.Option.ANY_ORDER |
                        PtnFilterChord.Option.AND_LOWER if and_lower else 0,
                exclude=False
            ).filter,
            combo_filter=PtnFilterCombo.create(
                [[0, 0]], keys=keys,
                options=PtnFilterCombo.Option.REPEAT,
                exclude=True).filter if not include_jack else None,
            type_filter=PtnFilterType.create(
                [[HoldTail, object]],
                options=PtnFilterType.Option.ANY_ORDER,
                exclude=True
            ).filter
        )
