from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

import numpy as np

from reamber.algorithms.pattern.filters.PtnFilter import PtnFilterType, PtnFilterCombo, PtnFilterChord
from reamber.base.Hold import HoldTail

if TYPE_CHECKING:
    from reamber.algorithms.pattern.combos import PtnCombo

class _PtnCChordStream:
    """ Fragment of PtnCombo """

    @abstractmethod
    def combinations(self, *args, **kwargs): ...

    def template_chord_stream(self: 'PtnCombo',
                              primary:int, secondary:int,
                              keys:int,
                              and_lower: bool = False,
                              include_jack: bool = False) -> np.ndarray:
        """ A template to quickly create chordstream lines

        The Primary and Secondary sizes are the size of each chord, then the subsequent one, the order doesn't matter.
        Jacks are automatically excluded unless

        All chord sizes below it are also included if ``andBelow is True``

        E.g. 1 a Jumpstream has ``primary=2, secondary=1``

        E.g. 2 a Handstream detection can use ``primary=3, secondary=2, andLower=True``. This means that you also accept
        ``primary=2, secondary=2``, ``primary=2, secondary=1``, ``primary=1, secondary=1``.

        :param primary: The primary chord size for each chord stream.
        :param secondary: The secondary chord size for each chord stream.
        :param keys: The keys of the map, used to detect pattern limits.
        :param and_lower: Whether to include lower size chords or not
        :param include_jack: Whether to include jackstreams or not
        :return:
        """

        return self.combinations(
            size=2,
            flatten=True,
            make_size2=True,
            chord_filter=PtnFilterChord.create(
                [[primary, secondary]], keys=keys,
                options=PtnFilterChord.Option.ANY_ORDER | PtnFilterChord.Option.AND_LOWER if and_lower else 0,
                exclude=False).filter,
            combo_filter=PtnFilterCombo.create(
                [[0, 0]], keys=keys,
                options=PtnFilterCombo.Option.REPEAT,
                exclude=True).filter if not include_jack else None,
            type_filter=PtnFilterType.create(
                [[HoldTail, object]], keys=keys,
                options=PtnFilterType.Option.ANY_ORDER,
                exclude=True).filter)
