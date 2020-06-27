from reamber.base.RAConst import RAConst
from typing import Callable, List, Union
from reamber.algorithms.generate.sv.generators.svFuncSequencer import svFuncSequencer
from reamber.osu.OsuBpmObj import OsuBpmObj
from reamber.osu.OsuSvObj import OsuSvObj,MAX_SV,MIN_SV

from copy import deepcopy

def svOsuMeasureLineC(firstOffset: float,
                      lastOffset: float,
                      funcs: List[Callable[[float], float]],
                      paddingSize: int = 10,
                      referenceBpm: float = 200,
                      stopBpm: float = 0.000000001,
                      fillBpm: float or None = 99999999,
                      startX: float = 0,
                      endX: float = 1) -> List[Union[OsuSvObj, OsuBpmObj]]:
    """ Generates Measure Line movement for osu! maps. Version 3. Inspired by datoujia

    This one directly returns svs and bpms due to the nature of the algorithm requiring osu! objects.

    This could output as Quaver but it has negative scroll

    ``S{_}...D{F},S{_}...D{F}_,...``

    :param firstOffset: The first Offset to start the function (x = startX)
    :param lastOffset: The last Offset to end the function (x = endX)
    :param funcs: The functions to use. startX <= x <= endX will be called, expecting a BPM as an output. \
        The more functions you have, the "laggier" it will be.
    :param paddingSize: The size of the padding, the larger the value, the lower the FPS
    :param referenceBpm: The bpm value referenced for Bpms.
    :param stopBpm: The bpm value for stop Bpms. Cannot be 0.
    :param fillBpm: The bpm to use to fill such that the sequence ends on lastOffset. None for no fill.
    :param startX: The starting X to use
    :param endX: The ending X to use
    """

    # DO NOT CHANGE ANY OF THESE, THESE ARE OPTIMIZED VALUES.

    # The higher the factor, the laggier it is, we optimized it such that it uses just the right amount of lines.
    # How I got the values? Guess and Check.
    DIVISION_FACTOR = 12 * (len(funcs) + 1) / referenceBpm
    SDF = 50 * DIVISION_FACTOR
    sdfBpm = 100 * SDF * referenceBpm

    # DO NOT CHANGE ANY OF THESE, THESE ARE OPTIMIZED VALUES.

    totalGaps = RAConst.mSecToMin(sdfBpm)  # The number of measure lines/gaps generated.
    totalSv = totalGaps * MIN_SV  # The total area covered by all svs.

    # Append a y = 0 to get diff on first func
    funcs_ = [lambda x: 0, *funcs]
    funcDiff = []
    for funcI in range(len(funcs)):  # -1 due to the appended y = 0, -1 due to custom last func
        def f(x, i=funcI):
            sort = sorted([g(x) * totalSv / DIVISION_FACTOR for g in funcs_])
            for s in range(len(sort)):
                sort[s] = max(0, sort[s])  # We eliminate all negative inputs

            diff = [g2 - g1 for g1, g2 in zip(sort[:-1], sort[1:])]

            for d in range(len(diff)):
                if diff[d] < MIN_SV:
                    if d < len(diff) - 1:
                        diff[d + 1] -= MIN_SV - diff[d]
                    diff[d] = MIN_SV

            return diff[i]
        funcDiff.append(deepcopy(f))

    repeats = int((lastOffset - firstOffset) / (paddingSize + 3))

    bpmPkg = svFuncSequencer([stopBpm,
                              *[None for _ in range(paddingSize)],
                              sdfBpm,
                              None],
                             offsets=1,
                             repeatGap=2,
                             repeats=repeats).addOffset(firstOffset, inplace=False)

    svPkg = svFuncSequencer([*funcDiff, MAX_SV],
                            offsets=1 / totalGaps,
                            repeats=repeats,
                            repeatGap=2 + paddingSize + (1 - len(funcs) / totalGaps),
                            startX=startX,
                            endX=endX).addOffset(by=1 + paddingSize + firstOffset, inplace=False)

    # We clip the values here, just to optimize the output a bit
    svOsu = svPkg.combine().writeAsSv(OsuSvObj)
    for sv in svOsu:
        assert isinstance(sv, OsuSvObj)
        sv.multiplier = min(MAX_SV, sv.multiplier)
        sv.multiplier = max(MIN_SV, sv.multiplier)

    # Combines both sequence together and writes them as osu
    outList = [*bpmPkg.combine().writeAsBpm(OsuBpmObj, metronome=1), *svOsu]

    if fillBpm is not None:
        outList.extend([*[OsuBpmObj(x, fillBpm) for x in range(int(firstOffset + (3 + paddingSize) * repeats),
                                                               int(lastOffset))],
                        OsuBpmObj(lastOffset, referenceBpm)])
    else:
        outList.append(OsuBpmObj(int(firstOffset + (3 + paddingSize) * repeats), referenceBpm))

    return sorted(outList, key=lambda x: x.offset)

