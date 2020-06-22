"""

Notes: Last Measure Line in a 1ms
"""

from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.algorithms.generate.sv.SvPkg import SvPkg
from typing import Callable, List


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
    frameCount = int(duration / msecPerFrame)
    frames = SvPkg()
    funcCount = len(funcs)

    # frameCount // funcCount * funcCount this is to max sure that the offset doesn't exceed.
    # e.g. range(0, 5, 2) will cause a point on (4), where it will exceed 5.
    frame = SvSequence()
    for frameI in range(0, int(frameCount // funcCount * funcCount), funcCount):
        frame = SvSequence()

        for i, func in enumerate(funcs):
            frame.appendInit([(0 + i * msecPerFrame, teleportBpm),
                              *[(x + i * msecPerFrame, stopBpm) for x in range(2, 2 + paddingSize + 1)],
                              (3 + paddingSize + i * msecPerFrame, func(frameI / frameCount))])

        frames.seqs.append(frame.addOffset(msecPerFrame * frameI + firstOffset))

    # Fill missing ending to fit to lastOffset
    if fillBpm is not None:
        seqLastOffset = frame.lastOffset()
        frames.seqs.append(SvSequence([(offset, fillBpm) for offset in range(int(seqLastOffset + 1),
                                                                             int(lastOffset) + 1)]))

    return frames
