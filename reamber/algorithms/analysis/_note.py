""" This package handles all Note Analysis Functions """

from reamber.base.TimedObject import TimedObject
import pandas as pd
from typing import Union, List


def rollingDensity(objList: List[TimedObject], rollingWindowS: float = None) -> pd.DataFrame:
    """ Returns the Density DF for any list of TimedObjects

    :param objList: Any List of TimedObjects (Such as noteObjects from a map)
    :param rollingWindowS: The window to search in seconds. If left as None, the window is 0
    :return: Col 0 Offset (DateTime), Col 1 Density (Int)
    """
    df = pd.DataFrame([obj.offset for obj in objList])
    df = df.rename({0: 'offset'}, axis='columns')
    df['count'] = 1
    df['offset'] = pd.to_timedelta(df['offset'], unit='ms')
    df = df.groupby('offset').sum()
    if rollingWindowS is not None:
        df = df.rolling(f"{rollingWindowS}s").count()
        df['count'] /= rollingWindowS
        return df
    else:
        return df


def density(obj: Union[List[TimedObject], pd.DataFrame], denominatorS: float = 1.0) -> float:
    """ Returns the Density per Denominator(in seconds) """

    objLen = 0
    offsetLast = 0
    offsetFirst = 0
    if isinstance(obj, List):
        objSort = sorted(obj, key=lambda x: x.offset)
        objLen = len(obj)
        offsetLast = objSort[-1].offset
        offsetFirst = objSort[0].offset

    elif isinstance(obj, pd.DataFrame):
        obj = obj.sort_values('offset')
        objLen = len(obj)
        offsetLast  = obj['offset'].iloc[-1]
        offsetFirst = obj['offset'].iloc[0]

    return objLen * 1000 / ((offsetLast - offsetFirst) * denominatorS)

