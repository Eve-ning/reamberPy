from copy import deepcopy
from typing import Callable, List

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.algorithms.generate.sv.generators.svFuncSequencer import svFuncSequencer
from reamber.osu.OsuBpm import MIN_BPM

# The value to use when zero bpm is encountered, using osu's min
FALLBACK_ZERO_BPM = MIN_BPM

def svOsuMeasureLineA(firstOffset: float,
                      lastOffset: float,
                      funcs: List[Callable[[float], float]],
                      referenceBpm: float,
                      endBpm: float or None,
                      paddingSize: int = 10,
                      teleportBpm: float = 1e07,
                      stopBpm: float = 1e-05,
                      fillBpm: float or None = 1e-05,
                      startX: float = 0,
                      endX: float = 1) -> SvPkg:
    """ Generates Measure Line movement for osu! maps. Version 1.

    This is a beta function for svOsuMeasureLine, it may or may not work as expected.

    This handles multi functions a little bit better by stacking them in a single frame instead of flickering through
    them.

    Could be used for other VSRGs but if they support negative Scroll then it could be much easier.

    Sequence::

        S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,...

    :param firstOffset: The first Offset to start the function (x = startX)
    :param lastOffset: The last Offset to end the function (x = endX)
    :param funcs: The functions to use. startX <= x <= endX will be called, expecting a BPM as an output. \
        The more functions you have, the "laggier" it will be.
    :param referenceBpm: The bpm that is used to zero. Found by looking at BPM:XXX-XXX(Reference Bpm) in song select.
    :param paddingSize: The size of the padding, the larger the value, the lower the FPS
    :param teleportBpm: The bpm value for teleporting Bpms.
    :param stopBpm: The bpm value for stop Bpms. Cannot be 0.
    :param fillBpm: The bpm to use to fill such that the sequence ends on lastOffset. None for no fill.
    :param endBpm: The bpm to end the sequence with.
    :param startX: The starting X to use
    :param endX: The ending X to use
    """

    # Optimized value to make sure that 1.0 in input means at the top of the screen.
    # Not accurate for all scrolls and different hit positions.
    SCALING_FACTOR = 9311250 / referenceBpm

    # Append a y = 0 to get diff on first func
    funcs = [lambda x: 0, *funcs]
    funcDiff = []

    for funcI in range(len(funcs) - 1):  # -1 due to the appended y = 0, -1 due to custom last func
        def f(x, i=funcI):
            sort = sorted([g(x) * SCALING_FACTOR for g in funcs])
            for s in range(len(sort)):
                sort[s] = max(0.0, sort[s])  # We eliminate all negative inputs

            out = [g2 - g1 for g1, g2 in zip(sort[:-1], sort[1:])][i]
            if out == 0: return FALLBACK_ZERO_BPM
            else: return out
        funcDiff.append(deepcopy(f))

    funcSeq = []
    funcSeq.extend([stopBpm, *[None for _ in range(paddingSize)], funcDiff[0]])
    for func in funcDiff[1:]: funcSeq.extend([None, func])
    funcSeq.extend([None, stopBpm, None, teleportBpm])

    msecPerFrame = len(funcSeq)

    duration = lastOffset - firstOffset
    frameCount = int(duration / msecPerFrame)

    pkg = svFuncSequencer(funcs=funcSeq,
                          offsets=1,
                          repeats=frameCount,
                          repeatGap=1,
                          startX=startX,
                          endX=endX)

    pkg = SvPkg(map(lambda x: x.addOffset(firstOffset), pkg))

    # Fill missing ending to fit to lastOffset
    if fillBpm is not None:
        seqLastOffset = firstOffset + frameCount * msecPerFrame
        pkg.append(SvSequence([(offset, fillBpm) for offset in range(int(seqLastOffset), int(lastOffset))]))

    if endBpm is not None:
        pkg.append(SvSequence([(lastOffset, endBpm)]))

    return pkg
