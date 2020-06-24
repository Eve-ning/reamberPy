from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.base.lists.BpmList import BpmList


def svNormalizeBpm(bpms: BpmList,
                   normalizeTo: float) -> SvSequence:
    """ Generates Normalizing SVs for Bpm.

    Useful if Bpms are unexpectedly changing scroll speeds. Generated Scroll Velocities can counter it.

    :param bpms: Any Type of BpmList
    :param normalizeTo: The Bpm to normalize to
    """
    return SvSequence([(bpm.offset, normalizeTo / bpm.bpm) for bpm in bpms])
