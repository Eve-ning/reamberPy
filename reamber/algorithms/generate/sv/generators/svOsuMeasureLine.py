from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.algorithms.generate.sv.SvPkg import SvPkg
from typing import Callable, List
from reamber.algorithms.generate.sv.generators.svFuncSequencer import svFuncSequencer

from copy import deepcopy


# The value to use when zero bpm is encountered
FALLBACK_ZERO_BPM = 0.000000001

def svOsuMeasureLine1(firstOffset: float,
                      lastOffset: float,
                      funcs: List[Callable[[float], float]],
                      paddingSize: int = 10,
                      teleportBpm: float = 99999999,
                      stopBpm: float = 0.000000001,
                      fillBpm: float = 99999999,
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
    :param paddingSize: The size of the padding, the larger the value, the lower the FPS
    :param teleportBpm: The bpm value for teleporting Bpms.
    :param stopBpm: The bpm value for stop Bpms. Cannot be 0.
    :param fillBpm: The bpm to use to fill such that the sequence ends on lastOffset. None for no fill.
    :param startX: The starting X to use
    :param endX: The ending X to use
    """

    # Append a y = 0 to get diff on first func
    funcs = [lambda x: 0, *funcs]
    funcDiff = []

    for funcI in range(len(funcs) - 1):  # -1 due to the appended y = 0, -1 due to custom last func
        def f(x, i=funcI):
            sort = sorted([g(x) for g in funcs])
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
        pkg.append(SvSequence([(offset, fillBpm) for offset in range(int(seqLastOffset),
                                                                    int(lastOffset) + 1)]))

    return pkg


def svOsuMeasureLine2(firstOffset: float,
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

        T_S{S}...F,T_S{S}...F,T_S{S}...F,...

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
        pkg = svFuncSequencer(funcs=[teleportBpm, None, *[stopBpm for _ in range(paddingSize + 1)], func],
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
