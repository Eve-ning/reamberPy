"""

Notes: Last Measure Line in a 1ms
"""

from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.algorithms.generate.sv.SvPkg import SvPkg
from typing import Callable, List
from math import ceil


def svOsuMeasureLine(firstOffset: float,
                     lastOffset: float,
                     func: Callable[[float], float],
                     paddingSize: int = 0,
                     teleportBpm: float = 999999,
                     stopBpm: float = 0.001) -> SvPkg:
    """ Generates Measure Line movement for osu! maps.

    Could be used for other VSRGs but if they support negative Scroll then it could be much easier.

    Regardless, it'll returns a Sequence.

    :param firstOffset: The first Offset to start the function (x = 0)
    :param lastOffset: The last Offset to end the function (x = 1)
    :param func: The function to use. 0 <= x <= 1 will be called, expecting a BPM as an output
    :param paddingSize: The size of the padding, the larger the value, the lower the FPS
    :param teleportBpm: The bpm value for teleporting Bpms.
    :param stopBpm: The bpm value for stop Bpms. Cannot be 0.
    """

    # T S___F,T S___F,...
    msecPerFrame = 4 + paddingSize

    duration = lastOffset - firstOffset
    frameCount = int(duration / msecPerFrame)
    frames = SvPkg()

    for frameI in range(0, frameCount):
        frame = SvSequence([(0, teleportBpm),
                            *[(i, stopBpm) for i in range(2, 2 + paddingSize + 1)],
                            (2 + paddingSize + 1, func(frameI / frameCount))])

        frames.seqs.append(frame.addOffset(msecPerFrame * frameI + firstOffset))

    return frames
