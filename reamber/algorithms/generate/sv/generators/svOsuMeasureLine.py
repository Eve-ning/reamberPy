"""

Notes: Last Measure Line in a 1ms
"""

from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.algorithms.generate.sv.SvPkg import SvPkg
from typing import Callable, List
from reamber.algorithms.generate.sv.generators.svFuncSequencer import svFuncSequencer


def svOsuMeasureLine(firstOffset: float,
                     lastOffset: float,
                     funcs: List[Callable[[float], float]],
                     paddingSize: int = 10,
                     teleportBpm: float = 999999,
                     stopBpm: float = 0.001,
                     fillBpm: float = 999999) -> SvPkg:
    """ Generates Measure Line movement for osu! maps.

    Could be used for other VSRGs but if they support negative Scroll then it could be much easier.

    Regardless, it'll returns a Sequence.

    :param firstOffset: The first Offset to start the function (x = 0)
    :param lastOffset: The last Offset to end the function (x = 1)
    :param funcs: The functions to use. 0 <= x <= 1 will be called, expecting a BPM as an output. \
        The more functions you have, the "laggier" it will be.
    :param paddingSize: The size of the padding, the larger the value, the lower the FPS
    :param teleportBpm: The bpm value for teleporting Bpms.
    :param stopBpm: The bpm value for stop Bpms. Cannot be 0.
    :param fillBpm: The bpm to use to fill such that the sequence ends on lastOffset. None for no fill.
    """

    # T S___F,T S___F,...
    msecPerFrame = 4 + paddingSize

    duration = lastOffset - firstOffset
    frameCount = int(duration / (msecPerFrame * len(funcs)))

    pkgLastOffset = 0

    pkgs = SvPkg([])
    for funcI, func in enumerate(funcs):
        pkg = svFuncSequencer(funcs=[teleportBpm, None, *[stopBpm for _ in range(paddingSize + 1)], func],
                                     offsets=1,
                                     repeats=frameCount,
                                     repeatGap=1 + msecPerFrame,
                                     startX=0,
                                     endX=1,
                                     includeEnd=True)
        pkgs.extend(SvPkg(map(lambda x: x.addOffset(funcI * msecPerFrame + firstOffset), pkg)))

    # Fill missing ending to fit to lastOffset
    if fillBpm is not None:
        seqLastOffset = firstOffset + frameCount * msecPerFrame * len(funcs)
        pkgs.append(SvSequence([(offset, fillBpm) for offset in range(int(seqLastOffset),
                                                                      int(lastOffset) + 1)]))

    return pkgs
