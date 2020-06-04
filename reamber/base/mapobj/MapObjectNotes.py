from __future__ import annotations
from reamber.base.HitObject import HitObject
from reamber.base.HoldObject import HoldObject
from typing import TypeVar

HitBase = TypeVar("HitBase", bound=HitObject)
HoldBase = TypeVar("HoldBase", bound=HoldObject)


class MapObjectNotes:
    pass

