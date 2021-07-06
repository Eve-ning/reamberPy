from typing import Callable, List, Tuple

from reamber.algorithms.generate.sv.generators.svFuncSequencer import svFuncSequencer
from reamber.base.RAConst import RAConst
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuSv import OsuSv, MAX_SV, MIN_SV

from copy import deepcopy

def svOsuMeasureLineB(firstOffset: float,
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
    """ Generates Measure Line movement for osu! maps. Version 2. Inspired by datoujia

    Algorithm C implements collapsing, check that one out too, details enclosed there.

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
    funcs_ = [lambda x: 0, *funcs]
    funcDiff = []
    for funcI in range(len(funcs)):  # -1 due to the appended y = 0, -1 due to custom last func
        def f(x, i=funcI):
            # This sorts the algorithm's outputs so that we can find the difference without any negatives.
            sort = sorted([(g(x) - startY) / (endY - startY) * SCALING_FACTOR  for g in funcs_])

            # We eliminate all "negative" inputs. Anything below startY is negated.
            for s in range(len(sort)): sort[s] = max(0.0, sort[s])

            # Grab differences by doing a stagger loop
            diff = [g2 - g1 for g1, g2 in zip(sort[:-1], sort[1:])]

            # From here, we find out if the difference is < MIN_SV
            # To compensate for the < MIN_SV issue, the error is moved to the next SV
            for d in range(len(diff)):
                if diff[d] < MIN_SV:
                    if d < len(diff) - 1:
                        diff[d + 1] -= MIN_SV - diff[d]
                    diff[d] = MIN_SV

            return diff[i]
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
                             repeats=repeats).add_offset(firstOffset, inplace=False)

    svPkg = svFuncSequencer([*funcDiff, MAX_SV],
                            offsets=1 / totalGaps,
                            repeats=repeats,
                            repeatGap=2 + paddingSize + (1 - len(funcs) / totalGaps),
                            startX=startX,
                            endX=endX).add_offset(by=1 + paddingSize + firstOffset, inplace=False)

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

