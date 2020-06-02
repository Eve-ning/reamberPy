from pandas import DataFrame
from typing import List, Dict

from reamber.base.MapObject import MapObject
from dataclasses import asdict


def asDataFrame(obj: MapObject) -> Dict[str, DataFrame]:
    """ Converts a MapObject to a Dictionary of DataFrames

    :param obj: Any MapObject
    :return: A Dictionary of DataFrames
    """
    out: Dict = {}
    for key, item in obj.__dict__.items():
        if not isinstance(item, List): continue  # Don't create DF for singles
        try:
            out[key] = DataFrame([asdict(o) for o in item])
        except TypeError:  # asdict would throw this
            continue
        except Exception as e:  # This should be some other error
            print(e)
    return out




