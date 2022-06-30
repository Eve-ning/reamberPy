from fractions import Fraction

from reamber.algorithms.timing.TimingMap import TimingMap
from reamber.algorithms.timing.utils.BpmChangeSnap import BpmChangeSnap
from reamber.algorithms.timing.utils.snap import Snap

tm = TimingMap.from_bpm_changes_snap(0,[
    BpmChangeSnap(bpm=145.0, metronome=4,
                  snap=Snap(measure=0, beat=Fraction(0, 1), metronome=4)),
    BpmChangeSnap(bpm=1, metronome=4,
                  snap=Snap(measure=65.0, beat=Fraction(0, 1), metronome=4)),
    # BpmChangeSnap(bpm=175.0, metronome=4,
    #               snap=Snap(measure=66.0, beat=Fraction(0, 1), metronome=4))
])
#%%
tm.bpm_changes_snap
#%%
tm.bpm_changes_snap[0].measure_length * 65

#%%
