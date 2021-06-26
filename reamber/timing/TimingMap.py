from dataclasses import dataclass, field
from typing import List

import numpy as np
import pandas as pd

from reamber.base import RAConst
from reamber.timing import Measure

class TimingMap:
    """ This will decide the placement of the measures

    There is one important assumption, BPM Points will ONLY be on beats
    """

    df: pd.DataFrame
    divisions: List[int]
    beats_per_measure: List[int]
    slots_per_beat: int

    def __init__(self, divisions: List[int], beats_per_measure: List[int]):
        self.divisions = divisions
        self.beats_per_measure = beats_per_measure
        
        max_slots = max(divisions)

        # 8 measures, 4 beats, 4 b, 3 b , ...

        """ Here we create the offset triangle """

        assert max_slots > 0, f"max_slots cannot be less than 0. {max_slots}"

        # Creates the division triangle
        ar = np.zeros([max_slots, max_slots])
        for i in range(max_slots):
            ar[i, :i + 1] = np.linspace(0, 1, i + 1, endpoint=False)

        # Prunes the repeated slots
        visited = []
        for i in range(max_slots):
            for j in range(max_slots):
                if ar[i, j] in visited:
                    ar[i, j] = np.nan
                else:
                    visited.append(ar[i, j])

        exclude = np.arange(max_slots)[np.isin(np.arange(1, max_slots + 1), divisions, invert=True)]
        # Excludes any unwanted snaps
        for exc in exclude:
            assert exc > 0, f"Excluded snap cannot be 0 or less, {exclude}"
            ar[exc] = np.nan

        ar = np.stack([ar, *np.indices(ar.shape)])
        ar = ar[:, ~np.isnan(ar[0])].T

        self.slots_per_beat = ar.shape[0]

        measures = []

        for measure, b in enumerate(beats_per_measure):
            beats_ar = np.repeat(np.arange(b), ar.shape[0])[..., np.newaxis]
            measure_ar = np.ones_like(beats_ar) * measure
            measures.append(np.hstack([np.tile(ar, [b, 1]),
                                       beats_ar,
                                       measure_ar]))
        df = pd.DataFrame(np.vstack(measures),
                          columns=["offset", "division", "slot", "beat", "measure"])

        df['beat_length'] = np.nan
        df = df.sort_values(['measure','beat','offset'])
        df = df.reset_index(drop=True)
        self.df = df


    def time_by_snap(self,
                     bpms     :List[float] = (),
                     measures :List[int] = (),
                     beats    :List[int] = (),
                     divisions:List[int] = (),
                     slots    :List[int] = (),
                     offset_shift: float = 0
                     ):
        """ Sets the BPMS

        The ultimate length is determined by bpms

        """
        for s, d in zip(slots, divisions):
            assert s < d, "The slot used must always be less than the division"
            assert d > 0, "The division must always be positive"

        divisions = [d - 1 for d in divisions]

        features = (bpms, measures, beats, divisions, slots)
        count = len(bpms)
        ar = np.zeros([count, len(features)])
        for e, f in enumerate(features):
            ar[0:len(f), e] = f

        for i in range(count):
            mask = (self.df.measure  == ar[i, 1]) &\
                   (self.df.beat     == ar[i, 2]) &\
                   (self.df.division == ar[i, 3]) &\
                   (self.df.slot     == ar[i, 4])

            assert np.any(mask), f"Snap provided doesn't exist. " \
                                 f"Measure:{ar[i, 1]}, " \
                                 f"Beat:{ar[i, 2]}, " \
                                 f"Division:{ar[i, 3]}, " \
                                 f"Slot:{ar[i, 4]}" \

            self.df.loc[mask, 'beat_length']\
                = RAConst.MIN_TO_MSEC / ar[i, 0]

        self.finalize_offset(offset_shift=offset_shift)

    def time_by_offset(self,
                       bpms    :List[float] = (),
                       offsets :List[float] = (),
                       error_threshold: float = None):
        """ Sets the BPMS

        The ultimate length is determined by bpms

        """
        offsets = np.asarray(offsets)
        min_offset = np.min(offsets)
        offsets -= min_offset

        def insert_to_closest(offset_rel: float, beat: int, measure: int, beat_length: float):
            mask = (self.df.measure  == measure) &\
                   (self.df.beat     == beat)
            diff = np.abs(self.df.loc[mask].offset - offset_rel)
            mask = mask & (diff == np.min(diff))

            self.df.loc[mask, 'beat_length'] = beat_length

            assert np.any(mask), f"Snap provided doesn't exist. " \
                                 f"Measure:{measure}, " \
                                 f"Beat:{beat}, " \
                                 f"Relative Offset:{offset_rel}" \

        beat_lengths = RAConst.MIN_TO_MSEC / np.asarray(bpms)

        prev_beat_length = beat_lengths[0]
        prev_offset = offsets[0]
        prev_beat_per_measure = self.beats_per_measure[0]
        insert_to_closest(0, 0, 0, prev_beat_length)

        for beat_length, offset, beat_per_measure in \
            zip(beat_lengths[1:], offsets[1:], self.beats_per_measure[1:]):
            beats_to_next = (offset - prev_offset) / prev_beat_length
            measure = int(beats_to_next // prev_beat_per_measure)
            beat = np.floor(beats_to_next - measure)
            offset_rel = beats_to_next - measure - beat
            insert_to_closest(offset_rel, beat, measure, beat_length)

            prev_beat_length = beat_length
            prev_offset = offset
            prev_beat_per_measure = beat_per_measure

        self.finalize_offset(offset_shift=min_offset)

    def finalize_offset(self, offset_shift):
        self.df = self.df.ffill(axis=0).bfill(axis=0)

        TEMP_COL = 'temp'
        self.df[TEMP_COL] = 0
        offset = 0
        self.df.iloc[0, -1] = offset

        prev_offset = self.df.iloc[0].offset

        prev_beat = 0
        prev_measure = 0
        prev_beat_length = self.df.iloc[0].beat_length

        for i in self.df.iloc[1:].iterrows():
            r = i[1]

            if prev_beat != r.beat or prev_measure != r.measure:
                # If the beat/measure is different, then we consider the relative offset + 1.
                offset += (1 - prev_offset) * prev_beat_length
                prev_offset = 0
            else:
                offset += (r.offset - prev_offset) * prev_beat_length
                prev_offset = r.offset

            # Sets the temp row by -1 index
            self.df.iloc[i[0], -1] = offset

            prev_beat = r.beat
            prev_measure = r.measure
            prev_beat_length = r.beat_length

        self.df.offset = self.df[TEMP_COL]
        self.df = self.df.drop(TEMP_COL, axis=1)
        self.df.offset += offset_shift
        assert len(self.df.offset) == len(np.unique(self.df.offset)),\
            f"Unexpected Behaviour. {len(self.df.offset) - len(np.unique(self.df.offset))} Duplicated Offsets Detected."
