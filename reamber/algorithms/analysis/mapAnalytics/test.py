from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reamber.algorithms.analysis.mapAnalytics.MapAnalytics import MapAnalytics


class Hello:

    def __init__(self, ma: 'MapAnalytics'):
        self.ma = ma
        pass

    def p(self):
        print(self.ma.tot)

