from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.base.lists.BpmList import BpmList


def sv_normalize_bpm(bpms: BpmList,
                     normalize_to: float) -> SvSequence:
    """ Generates Normalizing SVs for Bpm.

    Useful if Bpms are unexpectedly changing scroll speeds. Generated Scroll Velocities can counter it.

    :param bpms: Any Type of BpmList
    :param normalize_to: The Bpm to normalize to
    """
    return SvSequence([(bpm.offset, normalize_to / bpm.bpm) for bpm in bpms])
