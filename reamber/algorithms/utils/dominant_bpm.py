import pandas as pd

from reamber.base import Map


def dominant_bpm(m: Map):
    """ Gets the dominant BPM

    Notes:
        The dominance is defined by the bpm that is active for the longest cumulative time.

    Args:
        m: Any Map Instance

    Returns:
        The dominant BPM as a np.float64
    """
    s = m.stack()
    return (
        pd
        # Append the last object offset of the note to the bpm offsets
        .concat([m.bpms.offset, pd.Series(s.offset.max())])
        # Sort in case it's not sorted
        .sort_values()
        # Get intervals between bpm
        .diff()
        # Drop NA created by diff
        .dropna()
        # Set index/axis to bpm for grouping
        .set_axis(m.bpms.bpm)
        # Group by the bpm
        .groupby(level=0)
        # Sum groups
        .sum()
        # Get the index/axis (bpm) that is maximum
        .idxmax()
    )
