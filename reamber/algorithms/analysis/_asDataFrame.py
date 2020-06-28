from pandas import DataFrame
from typing import List, Dict

from reamber.base.Map import Map
from dataclasses import asdict


def asDataFrame(obj: Map) -> Dict[str, DataFrame]:
    """ Converts a Map to a Dictionary of DataFrames

    :param obj: Any Map
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




