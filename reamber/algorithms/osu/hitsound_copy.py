import logging
from copy import deepcopy

import numpy as np
import pandas as pd

from reamber.osu.OsuMap import OsuMap
from reamber.osu.OsuSample import OsuSample

log = logging.getLogger(__name__)


def hitsound_copy(m_from: OsuMap, m_to: OsuMap,
                  inplace: bool = False) -> OsuMap:
    """Copies the hitsound from mFrom to mTo

    Args:
        inplace: Whether to just modify this instance or return a modified copy
        m_from: The map you want to copy from
        m_to: The map you want to copy to, it doesn't mutate this.
    :return: A copy of mTo with the copied hitsounds.
    """
    df_from = pd.concat([i.df for i in m_from.notes], sort=False)
    df_from = df_from.drop(['column', 'length'], axis='columns',
                           errors='ignore')
    df_from = df_from[(df_from['addition_set'] != 0) |
                      (df_from['custom_set'] != 0) |
                      (df_from['hitsound_set'] != 0) |
                      (df_from['sample_set'] != 0) |
                      (df_from['hitsound_file'] != "")]
    df_from: pd.DataFrame
    df_from = df_from.sort_values('offset').reset_index(drop=True)

    HITSOUND_CLAP = 2
    HITSOUND_FINISH = 4
    HITSOUND_WHISTLE = 8

    # Before we group, we want to split the hitsound_file to clap,
    # finish and whistle (2, 4, 8)
    df_from['hitsound_clap'] \
        = np.where(df_from['hitsound_set'] & HITSOUND_CLAP == HITSOUND_CLAP,
                   HITSOUND_CLAP, 0)
    df_from['hitsound_finish'] \
        = np.where(
        df_from['hitsound_set'] & HITSOUND_FINISH == HITSOUND_FINISH,
        HITSOUND_FINISH, 0)
    df_from['hitsound_whistle'] \
        = np.where(
        df_from['hitsound_set'] & HITSOUND_WHISTLE == HITSOUND_WHISTLE,
        HITSOUND_WHISTLE, 0)

    df_from = df_from.drop('hitsound_set', axis='columns')
    df_from = df_from.groupby('offset')

    # We'll just get the mTo data then export it again
    df = pd.concat([i.df for i in m_to.notes], sort=False)
    df = df.sort_values('offset').reset_index(drop=True)
    df_to_offsets = df['offset']

    # We grab a deepCopy if not inplace
    m_to_copy = m_to if inplace else deepcopy(m_to)
    m_to_copy.reset_samples()

    # The idea is to loop through unique offsets
    # where there's hitsounds/samples
    # For each offset, we group by the volume,
    # because we can snap multiple default samples if we just specify 1 volume

    # e.g. < (C)lap (F)inish (W)histle >
    # C F W  Vol | C F W  Vol
    # 1 0 0  20  | 1 1 1  20
    # 0 1 0  20  | 1 0 0  30
    # 0 0 1  20  | 0 1 1  40
    # 1 0 0  30  | CUSTOM 20
    # 0 1 1  40  |
    # CUSTOM 20  |

    for offset, offset_group in df_from:
        # You cannot have hitsound Files and the default hitsounds together
        # We find out which indexes match on the df we want to copy to
        slot_indexes = list(
            (df_to_offsets == offset)[df_to_offsets == offset].index)
        slot = 0  # Indicates the snap on "TO" we're looking at right now
        slot_max = len(slot_indexes)  # The maximum slots

        offset_group: pd.DataFrame
        v_groups = offset_group.groupby('volume', as_index=False) \
            .agg({'hitsound_file': ';'.join,
                  'hitsound_clap': 'sum',
                  'hitsound_finish': 'sum',
                  'hitsound_whistle': 'sum'})
        v_groups: pd.DataFrame

        for _, v_group in v_groups.iterrows():  # v_group -> Volume Group
            volume = v_group['volume']
            claps = int(v_group['hitsound_clap'] / HITSOUND_CLAP)
            finishes = int(v_group['hitsound_finish'] / HITSOUND_FINISH)
            whistles = int(v_group['hitsound_whistle'] / HITSOUND_WHISTLE)
            hitsound_files = [file for file in
                              v_group['hitsound_file'].split(';') if
                              len(file) > 0]

            samples = max(claps, finishes, whistles)
            for _ in range(samples):
                # We loop through the default C F W samples here
                if slot == slot_max:
                    log.debug(
                        f"No snap to place hitsound {slot} > {slot_max}, "
                        f"dropping hitsound at {offset}"
                    )
                    break

                val = 0
                if claps:
                    claps -= 1
                    val += HITSOUND_CLAP
                if finishes:
                    finishes -= 1
                    val += HITSOUND_FINISH
                if whistles:
                    whistles -= 1
                    val += HITSOUND_WHISTLE

                log.debug(f"Slotted Hitsound {val} at {offset} vol {volume}")
                df.at[slot_indexes[slot], 'hitsound_set'] = val
                df.at[
                    slot_indexes[slot], 'volume'] = volume if volume > 0 else 0
                slot += 1

            for file in hitsound_files:
                # We loop through the custom sample here
                if slot == slot_max:
                    log.debug(
                        f"No snap to place hitsound {slot} > {slot_max}, "
                        f"sampling {file} at {offset}"
                    )
                    m_to_copy.samples = m_to_copy.samples.append(
                        OsuSample(offset=offset, sample_file=file,
                                  volume=volume))
                    break
                log.debug(f"Slotted Hitsound {file} at {offset} vol {volume}")
                df.at[slot_indexes[slot], 'hitsound_file'] = file
                df.at[
                    slot_indexes[slot], 'volume'] = volume if volume > 0 else 0
                slot += 1

    if 'length' in df:
        m_to_copy.holds.df = df[~np.isnan(df.length)]
        m_to_copy.hits.df = df[np.isnan(df.length)].drop('length', axis=1)
    else:
        m_to_copy.hits.df = df

    return None if inplace else m_to_copy
