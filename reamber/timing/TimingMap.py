from typing import List

import numpy as np
import pandas as pd

from reamber.base import RAConst

class TimingMap:
    """ This will decide the placement of the measures

    There is one important assumption, BPM Points will ONLY be on beats
    """

    df: pd.DataFrame
    divisions: np.ndarray
    beats_per_measure: List[int]
    slots_per_beat: int

    def __init__(self, divisions: List[List[int]], beats_per_measure: List[int]):
        self.divisions = np.sort(np.asarray(divisions))
        self.beats_per_measure = beats_per_measure

        df = pd.concat([Measure.create_measure(d, b, e) for e, (d, b) in enumerate(zip(divisions, beats_per_measure))])

        df['beat_length'] = np.nan
        df.division += 1
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

        # divisions = [d - 1 for d in divisions]

        features = (bpms, measures, beats, divisions, slots)
        count = len(bpms)
        ar = np.zeros([count, len(features)])
        for e, f in enumerate(features):
            ar[0:len(f), e] = f

        for i in range(count):
            if ar[i, 4] == 0: ar[i, 3] = 1
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

        self._finalize(offset_shift=offset_shift)

    def time_by_offset(self,
                       bpms    :List[float] = (),
                       offsets :List[float] = (),
                       error_threshold: float = None):
        """ Sets the BPMS using offsets.

        This will attempt to find the closest snap for the offset provided

        """
        offsets = np.asarray(offsets)
        min_offset = np.min(offsets)
        offsets -= min_offset

        def insert_to_closest(offset_rel: float, beat: int, measure: int, beat_length: float):
            # Find exact match for measure & beat
            mask = (self.df.measure  == measure) &\
                   (self.df.beat     == beat)

            # Find nearest snap match for relative offset
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
            # For each entry, we calculate the
            # The number of beats so this current entry
            # The number of measures
            # The remainder (which will be best-matched to offset)
            beats_to_next = (offset - prev_offset) / prev_beat_length
            measure = int(beats_to_next // prev_beat_per_measure)
            beat = np.floor(beats_to_next - measure)
            offset_rel = beats_to_next - measure - beat
            insert_to_closest(offset_rel, beat, measure, beat_length)

            prev_beat_length = beat_length
            prev_offset = offset
            prev_beat_per_measure = beat_per_measure

        self._finalize(offset_shift=min_offset)

    def _finalize(self, offset_shift):
        self.df = self.df.ffill(axis=0).bfill(axis=0)

        offset = 0
        self.df.iloc[0, -1] = offset

        # prev_offset = self.df.iloc[0].offset
        #
        # prev_beat = 0
        # prev_measure = 0
        # prev_beat_length = self.df.iloc[0].beat_length
        # for i in self.df.iloc[1:].iterrows():
        #     r = i[1]
        #
        #     if prev_beat != r.beat or prev_measure != r.measure:
        #         # If the beat/measure is different, then we consider the relative offset + 1.
        #         offset += (1 - prev_offset) * prev_beat_length
        #         prev_offset = 0
        #     else:
        #         offset += (r.offset - prev_offset) * prev_beat_length
        #         prev_offset = r.offset
        #
        #     # Sets the temp row by -1 index
        #     self.df.iloc[i[0], -1] = offset
        #
        #     prev_beat = r.beat
        #     prev_measure = r.measure
        #     prev_beat_length = r.beat_length
        #
        # self.df.offset = self.df[TEMP_COL]
        # self.df = self.df.drop(TEMP_COL, axis=1)

        diff = np.diff(self.df.offset, prepend=0)
        diff = np.where(diff < 0, diff + 1, diff)
        self.df.offset = np.cumsum(diff * self.df.beat_length)
        self.df['bpm'] = RAConst.MIN_TO_MSEC / self.df.beat_length
        self.df = self.df.drop('beat_length', axis=1)
        self.df.offset += offset_shift
        assert len(self.df.offset) == len(np.unique(self.df.offset)),\
            f"Unexpected Behaviour. {len(self.df.offset) - len(np.unique(self.df.offset))} Duplicated Offsets Detected."
        self.df['obj'] = [[] for _ in range(len(self.df))]

    def get_offset(self, offset: float) -> list:
        diff = np.abs(self.df.offset - offset)
        ix = np.argmin(diff)
        return self.df.iloc[ix, -1]

    def get_snap(self, measure=0, beat=0, slot=0, division=0) -> list:
        mask = (self.df.measure == measure) &\
               (self.df.beat == beat) &\
               (self.df.slot == slot) &\
               (self.df.division == division)
        return self.df[mask].iloc[0,-1]

    def append_offset(self, obj: object, offset: float):
        self.get_offset(offset).append(obj)

    def append_snap(self, obj: object, measure=0, beat=0, slot=0, division=0):
        print(measure, beat, slot, division)
        self.get_snap(measure=measure,
                      beat=beat,
                      slot=slot,
                      division=division).append(obj)


class Measure:

    @staticmethod
    def create_measure(divisions: List[int], beats, measure):
        divisions = np.asarray(divisions)
        if 1 not in divisions:
            divisions = np.append(divisions, 1)

        max_slots = max(divisions)

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

        # Stacks indices
        ar = np.stack([ar, *np.indices(ar.shape)])

        # Removes redundant divs
        ar = ar[:, divisions - 1].reshape([3, -1])

        # Removes NaNs
        ar = ar[:, ~np.isnan(ar[0])].T

        # Creates Beats and Measure Cols
        beats_ar = np.repeat(np.arange(beats), ar.shape[0])[..., np.newaxis]
        measure_ar = np.ones_like(beats_ar) * measure

        # Pre-stack sort
        ar = np.sort(ar, axis=0)

        # Stacks the beats and measures
        c = np.hstack([np.tile(ar, [beats, 1]), beats_ar, measure_ar])

        # Create DF
        df = pd.DataFrame(np.vstack(c),
                          columns=["offset", "division", "slot", "beat", "measure"])

        return df
