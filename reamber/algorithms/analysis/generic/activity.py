from reamber.base.BpmObj import BpmObj
from reamber.base.lists.TimedList import TimedList
from reamber.base.TimedObj import TimedObj
from typing import Tuple, List

def activity(tl: TimedList, lastOffset:float = None) -> List[Tuple[TimedObj, float]]:
    """ Calculates how long each Timed Object is active

    For example:

    The algorithm calculates this::

        SEC 1   2   3   4   5   6   7   8   9
        BPM 100 ------> 200 --> 300 -------->

    returns [(TimedObj<100>, 3000), (TimedObj<200>, 2000), (TimedObj<300>, 3000)]

    :param tl: Timed List
    :param lastOffset: Last offset, if None, uses TimedObj.lastOffset()
    :return A List of Tuples in the format [(TimedObj, Activity In ms), ...]
    """

    if lastOffset is None: lastOffset = tl.lastOffset()

    # Describes the BPM and Length of it active
    # e.g. [(120.0, 2000<ms>), (180.0, 1000<ms>), ...]
    tlLen: List[Tuple[BpmObj, float]] = []

    for obj in tl.sorted(reverse=True).data():
        if obj.offset >= lastOffset:
            tlLen.append((obj, 0.0))  # If the BPM doesn't cover any notes it is inactive
        else:
            tlLen.append((obj, lastOffset - obj.offset))
            lastOffset = obj.offset
    return tlLen
