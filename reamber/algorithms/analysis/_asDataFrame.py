from pandas import DataFrame
from typing import List, Dict

from reamber.base.MapObj import MapObj
from dataclasses import asdict


def asDataFrame(obj: MapObj) -> Dict[str, DataFrame]:
    """ Converts a MapObj to a Dictionary of DataFrames

    :param obj: Any MapObj
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




