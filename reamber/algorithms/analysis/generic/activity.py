from reamber.base.Bpm import Bpm
from reamber.base.lists.TimedList import TimedList
from reamber.base.Timed import Timed
from typing import Tuple, List

def activity(tl: TimedList, lastOffset:float = None) -> List[Tuple[Timed, float]]:
    """ Calculates how long each Timed Object is active. Implicitly sorts object by offset

    For example:

    The algorithm calculates this::

        SEC 1   2   3   4   5   6   7   8   9
        BPM 100 ------> 200 --> 300 -------->

    returns [(Timed<100>, 3000), (Timed<200>, 2000), (Timed<300>, 3000)]

    :param tl: Timed List
    :param lastOffset: Last offset, if None, uses Timed.lastOffset()
    :return A List of Tuples in the format [(Timed, Activity In ms), ...]
    """

    if lastOffset is None: lastOffset = tl.lastOffset()

    # Describes the BPM and Length of it active
    # e.g. [(120.0, 2000<ms>), (180.0, 1000<ms>), ...]
    acts: List[Tuple[Bpm, float]] = []

    for obj in tl.sorted(reverse=True).data():
        if obj.offset >= lastOffset:
            acts.append((obj, 0.0))  # If the BPM doesn't cover any notes it is inactive
        else:
            acts.append((obj, lastOffset - obj.offset))
            lastOffset = obj.offset
    return list(reversed(acts))
