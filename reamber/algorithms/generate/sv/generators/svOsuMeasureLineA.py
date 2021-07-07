from copy import deepcopy
from typing import Callable, List

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence
from reamber.algorithms.generate.sv.generators.svFuncSequencer import sv_func_sequencer
from reamber.osu.OsuBpm import MIN_BPM

# The value to use when zero bpm is encountered, using osu's min
FALLBACK_ZERO_BPM = MIN_BPM

def sv_osu_measure_line_a(first_offset: float,
                          last_offset: float,
                          funcs: List[Callable[[float], float]],
                          reference_bpm: float,
                          end_bpm: float or None,
                          padding_size: int = 10,
                          teleport_bpm: float = 1e07,
                          stop_bpm: float = 1e-05,
                          fill_bpm: float or None = 1e-05,
                          start_x: float = 0,
                          end_x: float = 1) -> SvPkg:
    """ Generates Measure Line movement for osu! maps. Version 1.

    This is a beta function for svOsuMeasureLine, it may or may not work as expected.

    This handles multi functions a little bit better by stacking them in a single frame instead of flickering through
    them.

    Could be used for other VSRGs but if they support negative Scroll then it could be much easier.

    Sequence::

        S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,S_{_}...F{_F}..._S_T,...

    :param first_offset: The first Offset to start the function (x = startX)
    :param last_offset: The last Offset to end the function (x = endX)
    :param funcs: The functions to use. startX <= x <= endX will be called, expecting a BPM as an output. \
        The more functions you have, the "laggier" it will be.
    :param reference_bpm: The bpm that is used to zero. Found by looking at BPM:XXX-XXX(Reference Bpm) in song select.
    :param padding_size: The size of the padding, the larger the value, the lower the FPS
    :param teleport_bpm: The bpm value for teleporting Bpms.
    :param stop_bpm: The bpm value for stop Bpms. Cannot be 0.
    :param fill_bpm: The bpm to use to fill such that the sequence ends on last_offset. None for no fill.
    :param end_bpm: The bpm to end the sequence with.
    :param start_x: The starting X to use
    :param end_x: The ending X to use
    """

    # Optimized value to make sure that 1.0 in input means at the top of the screen.
    # Not accurate for all scrolls and different hit positions.
    SCALING_FACTOR = 9311250 / reference_bpm

    # Append a y = 0 to get diff on first func
    funcs = [lambda x: 0, *funcs]
    func_diff = []

    for func_i in range(len(funcs) - 1):  # -1 due to the appended y = 0, -1 due to custom last func
        def f(x, i=func_i):
            sort = sorted([g(x) * SCALING_FACTOR for g in funcs])
            for s in range(len(sort)):
                sort[s] = max(0.0, sort[s])  # We eliminate all negative inputs

            out = [g2 - g1 for g1, g2 in zip(sort[:-1], sort[1:])][i]
            if out == 0: return FALLBACK_ZERO_BPM
            else: return out
        func_diff.append(deepcopy(f))

    func_seq = []
    func_seq.extend([stop_bpm, *[None for _ in range(padding_size)], func_diff[0]])
    for func in func_diff[1:]: func_seq.extend([None, func])
    func_seq.extend([None, stop_bpm, None, teleport_bpm])

    msec_per_frame = len(func_seq)

    duration = last_offset - first_offset
    frame_count = int(duration / msec_per_frame)

    pkg = sv_func_sequencer(funcs=func_seq,
                            offsets=1,
                            repeats=frame_count,
                            repeat_gap=1,
                            start_x=start_x,
                            end_x=end_x)

    pkg = SvPkg(map(lambda x: x.add_offset(first_offset), pkg))

    # Fill missing ending to fit to last_offset
    if fill_bpm is not None:
        seqlast_offset = first_offset + frame_count * msec_per_frame
        pkg.append(SvSequence([(offset, fill_bpm) for offset in range(int(seqlast_offset), int(last_offset))]))

    if end_bpm is not None:
        pkg.append(SvSequence([(last_offset, end_bpm)]))

    return pkg
