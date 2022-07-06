from copy import deepcopy
from typing import Callable, List, Tuple

from reamber.algorithms.generate.sv.generators.svFuncSequencer import sv_func_sequencer
from reamber.base.RAConst import RAConst
from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuSv import OsuSv

MIN_SV, MAX_SV = 0.01, 10

def sv_osu_measure_line_c(first_offset: float,
                          last_offset: float,
                          funcs: List[Callable[[float], float]],
                          end_bpm: float,
                          padding_size: int = 10,
                          stop_bpm: float = 1e-05,
                          fill_bpm: float or None = 1e07,
                          start_x: float = 0,
                          end_x: float = 1,
                          start_y: float = 0,
                          end_y: float = 1
                          ) -> Tuple[List[OsuSv], List[OsuBpm]]:
    """ Generates Measure Line movement for osu! maps. Version 3. Inspired by datoujia

    This algorithm is largely similar to Algo B, but I added a collapsing feature.

    This is a separate algorithm to make the distinction clearer, and I believe Algo B may be useful
    in certain places as Algo C can cause flickering on collapse.

    This one directly returns svs and bpms due to the nature of the algorithm requiring osu! objects.

    This could output as Quaver but it has negative scroll

    ``S{_}...D{F},S{_}...D{F}_,...``

    :param first_offset: The first Offset to start the function (x = startX)
    :param last_offset: The last Offset to end the function (x = endX)
    :param funcs: The functions to use. startX <= x <= endX will be called, expecting a BPM as an output. \
        The more functions you have, the "laggier" it will be.
    :param end_bpm: The bpm value referenced for Bpms.
    :param padding_size: The size of the padding, the larger the value, the lower the FPS
    :param stop_bpm: The bpm value for stop Bpms. Cannot be 0.
    :param fill_bpm: The bpm to use to fill such that the sequence ends on last_offset. None for no fill.
    :param start_x: The starting X to use
    :param end_x: The ending X to use
    :param start_y: The starting Y to use
    :param end_y: The ending Y to use
    """

    # Optimized value to make sure that 1.0 in input means at the top of the screen.
    # Not accurate for all scrolls and different hit positions.
    SCALING_FACTOR = 1.175

    # Append a y = 0 to get diff on first func
    funcs_ = [lambda x: start_y, *funcs]
    func_diff = []

    # Gets the difference in functions here
    for func_i in range(len(funcs)):  # -1 due to the appended y = 0, -1 due to custom last func
        def f(x, i=func_i):
            # This sorts the algorithm's outputs so that we can find the difference without any negatives.
            sort = sorted([(g(x) - start_y) / (end_y - start_y) * SCALING_FACTOR for g in funcs_])

            # We eliminate all "negative" inputs. Anything below startY is negated.
            sort = [max(0.0, s) for s in sort]

            # Grab differences by doing a stagger loop
            diff = [g2 - g1 for g1, g2 in zip(sort[:-1], sort[1:])]

            # From here, we find out if the difference is < MIN_SV
            # Because the algorithm needs to collapse svs that are smaller than a threshold.
            for d in range(len(diff)):
                if diff[d] < MIN_SV:
                    if d != len(diff) - 1:
                        # Here, we spread the error to all svs after it.
                        # The amount of svs available is len(diff) - d
                        # E.g.
                        # [1] --Spread-> [2][3][4]
                        # All elements will receive error[1] / 3
                        diff[d + 1] += diff[d]
                    # Drop the current index by moving it out of bounds
                    diff[d] = MAX_SV

            return sorted(diff, key=lambda y: y == MAX_SV)[i]

        func_diff.append(deepcopy(f))

    dep_bpm = 60000 * (len(funcs) + 1)
    total_gaps = RAConst.msec_to_min(dep_bpm)  # The number of measure lines/gaps generated.

    repeats = int((last_offset - first_offset) / (padding_size + 3))

    bpm_pkg = sv_func_sequencer([stop_bpm,
                                *[None for _ in range(padding_size)],
                                dep_bpm,
                                None],
                               offsets=1,
                               repeat_gap=2,
                               repeats=repeats).add_offset(first_offset, inplace=False)

    sv_pkg = sv_func_sequencer([*func_diff, MAX_SV],
                              offsets=1 / total_gaps,
                              repeats=repeats,
                              repeat_gap=2 + padding_size + (1 - len(funcs) / total_gaps),
                              start_x=start_x,
                              end_x=end_x).add_offset(by=1 + padding_size + first_offset, inplace=False)

    # We clip the values here, just to optimize the output a bit
    sv_list = sv_pkg.combine().write_as_sv(OsuSv)
    for sv in sv_list:
        assert isinstance(sv, OsuSv)
        sv.multiplier = min(MAX_SV, sv.multiplier)
        sv.multiplier = max(MIN_SV, sv.multiplier)

    # Combines both sequence together and writes them as osu
    bpm_list = bpm_pkg.combine().write_as_bpm(OsuBpm, metronome=1)

    if fill_bpm is not None:
        bpm_list.extend([
            OsuBpm(last_offset, end_bpm),
            *[OsuBpm(x, fill_bpm) for x in range(int(first_offset + (3 + padding_size) * repeats),
                                                 int(last_offset))]])
    else:
        bpm_list.append(OsuBpm(int(first_offset + (3 + padding_size) * repeats), end_bpm))

    return sorted(sv_list), sorted(bpm_list)
