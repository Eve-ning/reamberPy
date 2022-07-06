import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Callable, List, Tuple

import numpy as np
import pandas as pd

from reamber.osu.OsuBpm import OsuBpm
from reamber.osu.OsuSv import OsuSv

log = logging.getLogger(__name__)

MIN_SV, MAX_SV = 0.01, 10


@dataclass
class SvOsuMeasureLineEvent:
    first_offset: float
    last_offset: float
    funcs: List[Callable[[float], float]]
    start_x: float = 0
    end_x: float = 1
    start_y: float = 0
    end_y: float = 1

    def evaluate(self, offsets: np.ndarray):
        """ Evaluates all functions at chosen offsets.

        Returns a DF"""

        # We scale the offset correctly for function evaluation.
        offsets_ = offsets[
            (self.first_offset <= offsets) & (offsets < self.last_offset)]

        frame = np.asarray([offsets_] * (len(self.funcs) + 1))
        frame = (frame - self.first_offset) / (
                self.last_offset - self.first_offset)
        for i, func in enumerate(self.funcs):
            # This really long statement just scales the offset so that it's within the defined xy bounds.
            frame[i + 1, :] = \
                (func(frame[i + 1, :] * (
                        self.end_x - self.start_x) + self.start_x) - self.start_y) \
                / (self.end_y - self.start_y)

        frame[0, :] = offsets_
        # print(frame)

        return pd.DataFrame(frame.transpose(), columns=['offset',
                                                        *[f"F{i}" for i in
                                                          range(
                                                              len(self.funcs))]])


def sv_osu_measure_line_md(events: List[SvOsuMeasureLineEvent],
                           first_offset: float,
                           last_offset: float,
                           end_bpm: float,
                           scaling_factor: float = 1.175,
                           padding_size: int = 10,
                           gap_bpm: float = 1e06,
                           stop_bpm: float = 1e-05,
                           fill_bpm: float or None = 1e06,
                           minimum: float = MIN_SV,
                           maximum: float = MAX_SV,
                           **kwargs) -> Tuple[List[OsuSv], List[OsuBpm]]:
    """ Generates Measure Line movement for osu! maps. Version 3. Inspired by datoujia

    This algorithm is largely similar to Algo B, but I added a collapsing feature.

    This is a separate algorithm to make the distinction clearer, and I believe Algo B may be useful
    in certain places as Algo C can cause flickering on collapse.

    This one directly returns svs and bpms due to the nature of the algorithm requiring osu! objects.

    This could output as Quaver but it has negative scroll

    ``S{_}...D{F},S{_}...D{F}_,...``

    :param events: The list of events to generate.
    :param first_offset: The first Offset to start the function (x = startX)
    :param last_offset: The last Offset to end the function (x = endX)
    :param end_bpm: The bpm value referenced for Bpms.
    :param scaling_factor: All svs will be scaled by this value, useful to zero out the 1.0 == the top of the map
    :param padding_size: The size of the padding, the larger the value, the lower the FPS
    :param gap_bpm: If there's a section where there are no svs to generate, use this bpm to fill.
    :param stop_bpm: The bpm value for stop Bpms. Cannot be 0.
    :param fill_bpm: The bpm to use to fill such that the sequence ends on last_offset. None for no fill.
    :param minimum: Minimum SV allowed. None or < MIN_SV will default to osu!'s minimum
    :param maximum: Maximum SV allowed. None will default to osu!'s maximum
    :param kwargs: Keyword arguments for Timing Point generation metadata. This can include metronome, however, some\
        will override this.
    """

    # We create another copy of kwargs guaranteed to not have metronome
    kwargs_ = deepcopy(kwargs)
    if "metronome" in kwargs_.keys():
        kwargs_.pop("metronome")

    offsets = np.arange(first_offset, last_offset - padding_size,
                        3 + padding_size)

    df: pd.DataFrame = pd.melt(
        pd.concat([e.evaluate(offsets) for e in events], sort=False),
        id_vars=['offset'])

    # Remove any row that is 0 or less since that doesn't contribute to the end result
    df = df[df['value'] > 0]

    # Here, we add a 0 on every offset because we want to take the difference later.
    df = pd.concat([df, pd.DataFrame({'offset': offsets, 'value': 0})],
                   sort=False)

    """
    1. Drop unused col variable
    2. Drop Na
    3. Groups by offset
    4. Then aggregates the grouping by making them into lists
    5. Move the index (the offset) to a column)
    """
    df = df \
        .drop(columns=['variable']) \
        .dropna() \
        .groupby('offset') \
        .agg(list) \
        .reset_index()

    offsets = df['offset'].to_numpy()
    vals = df['value'].to_numpy()

    svs = []
    bpms = []

    # Pre-process the minimum, cannot be smaller than MIN_SV
    minimum = max(MIN_SV, minimum)
    gap_filled = False

    for offset, val in zip(offsets, vals):
        val: list

        # The gap filling acts like a switch, if the gap is filled previously, it will not fill again until
        # len(val) is not 1. Where gap_filled will be False again.
        if len(val) == 1:
            log.debug(f"Empty Timestamp {offset:.2f}")
            if not gap_filled:
                bpms.append(OsuBpm(offset=offset, bpm=gap_bpm, **kwargs))
                log.debug(f"Adding Gap Bpm on {offset:.2f}")
                gap_filled = True
            continue
        gap_filled = False

        # We get the difference here with np, scaled with a factor
        diff = np.diff(sorted(val)) * scaling_factor

        log.debug(f"Before Diff Processing: {diff}")
        for d in range(len(diff)):
            if diff[d] < minimum:
                # If it's smaller than specified, we have to push the delta to the next diff
                if d != len(diff) - 1:
                    diff[d + 1] += diff[d]
                diff[d] = -1
            elif diff[d] > maximum:
                # If it's larger than specified, we just ignore it since it doesn't affect anything
                diff[d] = -1

        diff = np.asarray(diff[diff != -1])
        log.debug(f"After Diff Processing: {diff}")

        size = len(diff) + 1
        dep_bpm = 60000 * size

        log.debug(f"Adding Stop Bpm at: {offset:.2f}")
        log.debug(
            f"Adding Dep. Bpm {dep_bpm:.2f} at: {offset + padding_size + 1:.2f}")

        bpms.append(
            OsuBpm(offset=offset, bpm=stop_bpm, metronome=999, **kwargs_))
        bpms.append(
            OsuBpm(offset=offset + padding_size + 1, bpm=dep_bpm, metronome=1,
                   **kwargs_))
        for i, d in enumerate([*diff, MAX_SV]):
            log.debug(
                f"Adding Segment {d:.2f} at: {offset + padding_size + 1 + i / size:.2f}")

            svs.append(OsuSv(offset=offset + padding_size + 1 + i / size,
                             multiplier=d, **kwargs_))

    fill_from = max(offsets + padding_size + 2)

    for offset in range(int(fill_from), int(last_offset)):
        log.debug(f"Adding Fill Bpm at: {offset:.2f}")
        bpms.append(
            OsuBpm(offset=offset, bpm=fill_bpm, metronome=999, **kwargs_))

    log.debug(f"Adding End Bpm at: {last_offset:.2f}")
    bpms.append(OsuBpm(offset=last_offset, bpm=end_bpm, **kwargs))

    return svs, bpms
