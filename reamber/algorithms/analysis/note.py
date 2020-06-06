""" This package handles all Note Analysis Functions """

from reamber.base.TimedObj import TimedObj
from reamber.base.lists.TimedList import TimedList
import pandas as pd
from typing import Union, List


def rollingDensity(m: TimedList, rollingWindowS: float = None) -> pd.Series:
    """ Returns the Density DF for any list of TimedObjs

    :param m: Any Map
    :param rollingWindowS: The window to search in seconds. If left as None, the window is 0
    :return: Col 0 Offset (DateTime), Col 1 Density (Int)
    """
    df = m.df()
    df = df.rename({0: 'offset'}, axis='columns')
    df['count'] = 1
    df['offset'] = pd.to_timedelta(df['offset'], unit='ms')
    df = df.groupby('offset').sum()
    if rollingWindowS is not None:
        df = df.rolling(f"{rollingWindowS}s").count()
        df['count'] /= rollingWindowS
        return df.iloc[:, 0]
    else:
        return df.iloc[:, 0]


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

