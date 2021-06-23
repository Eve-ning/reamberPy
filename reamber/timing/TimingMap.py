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
                     slots    :List[int] = ()
                     ):
        """ Sets the BPMS

        The ultimate length is determined by bpms

        """
        for s, d in zip(slots, divisions):
            assert s < d, "The slot used must always be less than the division"
            assert s > 0, "The slot must always be positive"

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

    def time_by_offset(self,
                       bpms    :List[float] = (),
                       offset  :List[float] = (),
                       error_threshold: float = None):
        """ Sets the BPMS

        The ultimate length is determined by bpms

        """
        def closest_ix(offset: float):
            diff = np.abs(self.df.offset - offset)
            if error_threshold is not None:
                assert np.min(diff) < error_threshold, \
                    f"The error threshold was exceeded {error_threshold} < {np.min(diff)}"

            ix = np.argmin(diff)
        for bpm in bpms:

        pass

    def finalize_offset(self):
        self.df = self.df.ffill(axis=0).bfill(axis=0)
        offset = 0
        offset_rel = 0
        self.df['o'] = 0
        for i in self.df.iterrows():
            r = i[1]
            self.df.iloc[i[0], -1] = offset
            if r.offset <= offset_rel:
                # New beat/measure
                offset += (1 - offset_rel) * r.beat_length
            else:
                offset += (r.offset - offset_rel) * r.beat_length
            offset_rel = r.offset
        self.df.offset = self.df.o
        self.df = self.df.drop('o', axis=1)