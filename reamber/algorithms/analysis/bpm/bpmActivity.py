from reamber.base.Bpm import Bpm
from reamber.base.Map import Map
from reamber.algorithms.analysis.generic.activity import activity
from typing import Tuple, List


def bpmActivity(m: Map) -> List[Tuple[Bpm, float]]:
    """ Calculates how long the Bpm is active. Implicitly sorts BPM

    For example

    The algorithm calculates this::

        SEC 1   2   3   4   5   6   7   8   9
        BPM 100 ------> 200 --> 300 -------->

    returns [(BPMPoint<100>, 3000), (BPMPoint<200>, 2000), (BPMPoint<300>, 3000)]

    :param m: Map Object
    :return: A List of Tuples in the format [(BPMPoint, Activity In ms), ...]
    """

    # Guaranteed to return Bpm.
    # noinspection PyTypeChecker
    return activity(m.bpms, m.notes.lastOffset())
