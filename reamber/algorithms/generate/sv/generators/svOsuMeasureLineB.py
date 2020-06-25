from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.base.RAConst import RAConst
from typing import Callable, List
from reamber.algorithms.generate.sv.generators.svFuncSequencer import svFuncSequencer

from copy import deepcopy


# The value to use when zero bpm is encountered
FALLBACK_ZERO_BPM = 0.000000001


def svOsuMeasureLineB(firstOffset: float,
                     lastOffset: float,
                     funcs: List[Callable[[float], float]],
                     paddingSize: int = 10,
                     teleportBpm: float = 99999999,
                     stopBpm: float = 0.000000001,
                     fillBpm: float = 99999999,
                     startX: float = 0,
                     endX: float = 1) -> SvPkg:
    """ Generates Measure Line movement for osu! maps. Version 2

    Uses flickering to support multi functions. It's the more stable version.

    Could be used for other VSRGs but if they support negative Scroll then it could be much easier.

    Sequence::

        T_S{_}...F,T_S{_}...F,T_S{_}...F,...

    :param firstOffset: The first Offset to start the function (x = startX).
    :param lastOffset: The last Offset to end the function (x = endX).
    :param funcs: The functions to use. startX <= x <= endX will be called, expecting a BPM as an output. \
        The more functions you have, the "laggier" it will be.
    :param paddingSize: The size of the padding, the larger the value, the lower the FPS.
    :param teleportBpm: The bpm value for teleporting Bpms.
    :param stopBpm: The bpm value for stop Bpms. Cannot be 0.
    :param fillBpm: The bpm to use to fill such that the sequence ends on lastOffset. None for no fill.
    :param startX: The starting X to use
    :param endX: The ending X to use
    """

    msecPerFrame = 4 + paddingSize

    duration = lastOffset - firstOffset
    frameCount = int(duration / (msecPerFrame * len(funcs)))

    pkgs = SvPkg([])
    for funcI, func in enumerate(funcs):
        pkg = svFuncSequencer(funcs=[teleportBpm, None, stopBpm, *[None for _ in range(paddingSize)], func],
                              offsets=1,
                              repeats=frameCount,
                              repeatGap=1 + msecPerFrame,
                              startX=startX,
                              endX=endX)
        pkgs.extend(SvPkg(map(lambda x: x.addOffset(funcI * msecPerFrame + firstOffset), pkg)))

    # Fill missing ending to fit to lastOffset
    if fillBpm is not None:
        seqLastOffset = firstOffset + frameCount * msecPerFrame * len(funcs)
        pkgs.append(SvSequence([(offset, fillBpm) for offset in range(int(seqLastOffset),
                                                                      int(lastOffset) + 1)]))

    return pkgs
