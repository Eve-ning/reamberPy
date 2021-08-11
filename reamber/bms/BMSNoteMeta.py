from dataclasses import dataclass

from reamber.base import item_props


@item_props()
class BMSNoteMeta:

    _props = dict(sample=['b', 0])
