""" This package handles all Note Analysis Functions """

from reamber.base.lists.TimedList import TimedList
import pandas as pd
from typing import Union

def density(obj: Union[TimedList, pd.DataFrame], denominatorS: float = 1.0) -> float:
    """ Returns the Density per Denominator(in seconds) """

    objLen = 0
    offsetLast = 0
    offsetFirst = 0
    if isinstance(obj, TimedList):
        objSort = obj.sorted()
        objLen = len(obj.data())
        offsetLast = objSort.lastOffset()
        offsetFirst = objSort.firstOffset()

    elif isinstance(obj, pd.DataFrame):
        obj = obj.sort_values('offset')
        objLen = len(obj)
        offsetLast  = obj['offset'].iloc[-1]
        offsetFirst = obj['offset'].iloc[0]

    return objLen * 1000 / ((offsetLast - offsetFirst) * denominatorS)
