from reamber.base.MapObj import MapObj
from reamber.algorithms.analysis.bpm.bpmActivity import bpmActivity

def aveBpm(m: MapObj) -> float:
    """ Calculates the average BPM based on the BPM's Activity on notes

    Used in describe.

    """
    activitySum = 0
    sumProd = 0
    for bpm, activity in bpmActivity(m):
        activitySum += activity
        sumProd += bpm.bpm * activity
    return sumProd / activitySum
