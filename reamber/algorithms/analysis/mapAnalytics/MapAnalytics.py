""" This seeks to overhaul all separated classes/functions in analysis.

This will group everything under one singular class where just calling the function is needed. """

from __future__ import annotations
from reamber.algorithms.analysis.mapAnalytics.test import Hello
from abc import ABC, abstractmethod

class MapAnalytics(ABC):

    def hello(self):
        return Hello(self)



    pass
