""" This package handles all BPM Analysis Functions """
from reamber.base.BpmObj import BpmObj
from reamber.base.MapObj import MapObj
from typing import Tuple, List


def bpmActivity(m: MapObj) -> List[Tuple[BpmObj, float]]:
    """ Calculates how long the Bpm is active
    :return A List of Tuples in the format [(BPMPoint, Activity In ms), ...]
    """
    last = m.notes.lastOffset()

    # Describes the BPM and Length of it active
    # e.g. [(120.0, 2000<ms>), (180.0, 1000<ms>), ...]
    bpmLen: List[Tuple[BpmObj, float]] = []

    bpmRev = m.bpms.sorted()
    reversed(bpmRev)
    for bpm in bpmRev:
        if bpm.offset >= last:
            bpmLen.append((bpm, 0.0))  # If the BPM doesn't cover any notes it is inactive
        else:
            bpmLen.append((bpm, last - bpm.offset))
            last = bpm.offset
    return bpmLen


def aveBpm(m: MapObj) -> float:
    """ Calculates the average BPM based on the BPM's Activity on notes """
    activitySum = 0
    sumProd = 0
    for bpm, activity in bpmActivity(m):
        activitySum += activity
        sumProd += bpm.bpm * activity
    return sumProd / activitySum
