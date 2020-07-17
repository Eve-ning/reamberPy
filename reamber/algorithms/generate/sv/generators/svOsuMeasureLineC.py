from copy import deepcopy
from typing import Callable, List, Tuple

from reamber.algorithms.generate.sv.generators.svFuncSequencer import svFuncSequencer
from reamber.base.RAConst import RAConst
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuSv import OsuSv, MAX_SV, MIN_SV
from reamber.algorithms.generate.sv.SvPkg import SvPkg


def svOsuMeasureLineC(firstOffset: float,
                      lastOffset: float,
                      funcs: List[Callable[[float], float]],
                      endBpm: float,
                      paddingSize: int = 10,
                      stopBpm: float = 1e-05,
                      fillBpm: float or None = 1e07,
                      startX: float = 0,
                      endX: float = 1,
                      startY: float = 0,
                      endY: float = 1
                      ) -> Tuple[List[OsuSv], List[OsuBpm]]:
    """ Generates Measure Line movement for osu! maps. Version 3. Inspired by datoujia

    This algorithm is largely similar to Algo B, but I added a collapsing feature.

    This is a separate algorithm to make the distinction clearer, and I believe Algo B may be useful
    in certain places as Algo C can cause flickering on collapse.

    This one directly returns svs and bpms due to the nature of the algorithm requiring osu! objects.

    This could output as Quaver but it has negative scroll

    ``S{_}...D{F},S{_}...D{F}_,...``

    :param firstOffset: The first Offset to start the function (x = startX)
    :param lastOffset: The last Offset to end the function (x = endX)
    :param funcs: The functions to use. startX <= x <= endX will be called, expecting a BPM as an output. \
        The more functions you have, the "laggier" it will be.
    :param endBpm: The bpm value referenced for Bpms.
    :param paddingSize: The size of the padding, the larger the value, the lower the FPS
    :param stopBpm: The bpm value for stop Bpms. Cannot be 0.
    :param fillBpm: The bpm to use to fill such that the sequence ends on lastOffset. None for no fill.
    :param startX: The starting X to use
    :param endX: The ending X to use
    :param startY: The starting Y to use
    :param endY: The ending Y to use
    """

    # Optimized value to make sure that 1.0 in input means at the top of the screen.
    # Not accurate for all scrolls and different hit positions.
    SCALING_FACTOR = 1.175

    # Append a y = 0 to get diff on first func
    funcs_ = [lambda x: startY, *funcs]
    funcDiff = []

    # Gets the difference in functions here
    for funcI in range(len(funcs)):  # -1 due to the appended y = 0, -1 due to custom last func
        def f(x, i=funcI):

            # The error stack helps removing the error between 0 and any other sv.
            # This is helpful because when we remove a SV by shifting it out of bounds, we need to account for its
            # value.
            errorStack = 0.0

            sort = sorted([(g(x) - startY) / (endY - startY) * SCALING_FACTOR for g in funcs_])
            for s in range(len(sort)):
                sort[s] = max(startY, sort[s])  # We eliminate all negative inputs

            diff = [g2 - g1 for g1, g2 in zip(sort[:-1], sort[1:])]

            for d in range(len(diff)):
                if diff[d] < MIN_SV:
                    # If we want to remove it, we add its value to the errorStack, to be compensated by svs not affected
                    errorStack += diff[d]
                    diff[d] = MAX_SV
                else:
                    diff[d] += errorStack
                    errorStack = 0.0

            return sorted(diff, key=lambda x: x == MAX_SV)[i]

        funcDiff.append(deepcopy(f))

    depBpm = 60000 * (len(funcs) + 1)
    totalGaps = RAConst.mSecToMin(depBpm)  # The number of measure lines/gaps generated.

    repeats = int((lastOffset - firstOffset) / (paddingSize + 3))

    bpmPkg = svFuncSequencer([stopBpm,
                              *[None for _ in range(paddingSize)],
                              depBpm,
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
    svList = svPkg.combine().writeAsSv(OsuSv)
    for sv in svList:
        assert isinstance(sv, OsuSv)
        sv.multiplier = min(MAX_SV, sv.multiplier)
        sv.multiplier = max(MIN_SV, sv.multiplier)

    # Combines both sequence together and writes them as osu
    bpmList = bpmPkg.combine().writeAsBpm(OsuBpm, metronome=1)

    if fillBpm is not None:
        bpmList.extend([*[OsuBpm(x, fillBpm) for x in range(int(firstOffset + (3 + paddingSize) * repeats),
                                                               int(lastOffset))],
                        OsuBpm(lastOffset, endBpm)])
    else:
        bpmList.append(OsuBpm(int(firstOffset + (3 + paddingSize) * repeats), endBpm))

    return sorted(svList), sorted(bpmList)
