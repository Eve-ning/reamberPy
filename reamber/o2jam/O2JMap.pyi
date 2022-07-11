from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, TYPE_CHECKING

from reamber.base.Map import Map
from reamber.base.lists import TimedList
from reamber.o2jam.O2JEventPackage import O2JEventPackage
from reamber.o2jam.lists.O2JBpmList import O2JBpmList
from reamber.o2jam.lists.notes import O2JNoteList
from reamber.o2jam.lists.notes.O2JHitList import O2JHitList
from reamber.o2jam.lists.notes.O2JHoldList import O2JHoldList

if TYPE_CHECKING:
    from reamber.o2jam.O2JMapSet import O2JMapSet

import logging

log = logging.getLogger(__name__)


@dataclass
class O2JMap(Map[O2JNoteList, O2JHitList, O2JHoldList, O2JBpmList]):
    """This holds a single level of a .ojn file out of a total of three.

    This class only holds the data of notes and bpms. The rest can be found in the parent O2JMapSet instance.

    We won't support OJM, see why in O2JMapSet. """

    objs: Dict[str, TimedList] = \
        field(init=False,
              default_factory=lambda: dict(hits=O2JHitList([]),
                                           holds=O2JHoldList([]),
                                           bpms=O2JBpmList([])))

    @staticmethod
    def read_pkgs(pkgs: List[O2JEventPackage], init_bpm: float) -> O2JMap: ...

    # noinspection PyMethodOverriding
    def metadata(self, s: O2JMapSet, unicode=True, **kwargs) -> str: ...

    # noinspection PyMethodOverriding
    def describe(self, s: O2JMapSet, rounding: int = 2,
                 unicode: bool = False) -> str: ...
