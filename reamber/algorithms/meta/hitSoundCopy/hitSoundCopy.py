""" This is only for osu """
from reamber.osu.OsuMapObj import OsuMapObj
import pandas as pd
import numpy as np
import math

from reamber.osu.lists.notes.OsuHitList import OsuHitList, OsuHitObj
from reamber.osu.lists.notes.OsuHoldList import OsuHoldList, OsuHoldObj
from reamber.osu.lists.OsuNotePkg import OsuNotePkg
from reamber.osu.OsuSampleObj import OsuSampleObj

from copy import deepcopy

import logging
log = logging.getLogger(__name__)

def hitSoundCopy(mFrom: OsuMapObj, mTo: OsuMapObj, inplace: bool = False) -> OsuMapObj:
    """ Copies the hitsound from mFrom to mTo
    :param inplace: If true, mTo is modified
    :param mFrom: The map you want to copy from
    :param mTo: The map you want to copy to, it doesn't mutate this.
    :return: A copy of mTo with the copied hitsounds.
    """
    dfFrom = pd.concat([df for df in mFrom.notes.df().values()], sort=False)
    dfFrom = dfFrom.drop(['column', 'length'], axis='columns', errors='ignore')
    dfFrom = dfFrom[(dfFrom['additionSet'] != 0) |
                    (dfFrom['customSet'] != 0) |
                    (dfFrom['hitsoundSet'] != 0) |
                    (dfFrom['sampleSet'] != 0) |
                    (dfFrom['hitsoundFile'] != "")]
    dfFrom: pd.DataFrame
    dfFrom.sort_values('offset').reset_index(drop=True, inplace=True)

    HITSOUND_CLAP    = 2
    HITSOUND_FINISH  = 4
    HITSOUND_WHISTLE = 8

    # Before we group, we want to split the hitsoundFile to clap, finish and whistle (2, 4, 8)
    dfFrom['hitsoundClap']    = np.where(dfFrom['hitsoundSet'] & HITSOUND_CLAP == HITSOUND_CLAP, HITSOUND_CLAP, 0)
    dfFrom['hitsoundFinish']  = np.where(dfFrom['hitsoundSet'] & HITSOUND_FINISH == HITSOUND_FINISH, HITSOUND_FINISH, 0)
    dfFrom['hitsoundWhistle'] = np.where(dfFrom['hitsoundSet'] & HITSOUND_WHISTLE == HITSOUND_WHISTLE, HITSOUND_WHISTLE, 0)
    dfFrom.drop('hitsoundSet', inplace=True, axis='columns')
    dfFrom = dfFrom.groupby('offset')

    # We'll just get the mTo data then export it again
    dfToNotes = pd.concat(mTo.notes.df(), sort=False)
    dfToNotes.sort_values('offset').reset_index(drop=True, inplace=True)
    dfToOffsets = dfToNotes['offset']

    # We grab a deepCopy if not inplace
    mToCopy = mTo if inplace else deepcopy(mTo)
    mToCopy.resetAllSamples()

    # The idea is to loop through unique offsets where there's hitsounds/samples
    # For each offset, we group by the volume, because we can slot multiple default samples if we just specify 1 volume

    # e.g. < (C)lap (F)inish (W)histle >
    # C F W  Vol | C F W  Vol
    # 1 0 0  20  | 1 1 1  20
    # 0 1 0  20  | 1 0 0  30
    # 0 0 1  20  | 0 1 1  40
    # 1 0 0  30  | CUSTOM 20
    # 0 1 1  40  |
    # CUSTOM 20  |

    for offset, offsetGroup in dfFrom:
        # You cannot have hitsound Files and the default hitsounds together
        # We find out which indexes match on the df we want to copy to
        slotIndexes = list((dfToOffsets == offset)[dfToOffsets == offset].index)
        slot = 0  # Indicates the slot on "TO" we're looking at right now
        slotMax = len(slotIndexes)  # The maximum slots

        offsetGroup: pd.DataFrame
        vGroups = offsetGroup.groupby('volume', as_index=False)\
                             .agg({'hitsoundFile': ';'.join,
                                   'hitsoundClap': 'sum',
                                   'hitsoundFinish': 'sum',
                                   'hitsoundWhistle': 'sum'})
        vGroups: pd.DataFrame

        for k, vGroup in vGroups.iterrows():  # vGroup -> Volume Group
            volume   = vGroup['volume']
            claps    = int(vGroup['hitsoundClap'] / HITSOUND_CLAP)
            finishes = int(vGroup['hitsoundFinish'] / HITSOUND_FINISH)
            whistles = int(vGroup['hitsoundWhistle'] / HITSOUND_WHISTLE)
            hitsoundFiles = [file for file in vGroup['hitsoundFile'].split(';') if len(file) > 0]

            samples = max(claps, finishes, whistles)
            for i in range(0, samples):
                # We loop through the default C F W samples here
                if slot == slotMax:
                    log.debug(f"No slot to place hitsound {slot} > {slotMax}, dropping hitsound at {offset}")
                    break

                val = 0
                if claps:    claps -= 1;    val += HITSOUND_CLAP
                if finishes: finishes -= 1; val += HITSOUND_FINISH
                if whistles: whistles -= 1; val += HITSOUND_WHISTLE
                log.debug(f"Slotted Hitsound {val} at {offset} vol {volume}")
                dfToNotes.at[slotIndexes[slot], 'hitsoundSet'] = val
                dfToNotes.at[slotIndexes[slot], 'volume'] = volume if volume > 0 else 0
                slot += 1

            for file in hitsoundFiles:
                # We loop through the custom sample here
                if slot == slotMax:
                    log.debug(f"No slot to place hitsound {slot} > {slotMax}, sampling {file} at {offset}")
                    mToCopy.samples.append(OsuSampleObj(offset=offset, sampleFile=file, volume=volume))
                    break
                log.debug(f"Slotted Hitsound {file} at {offset} vol {volume}")
                dfToNotes.at[slotIndexes[slot], 'hitsoundFile'] = file
                dfToNotes.at[slotIndexes[slot], 'volume'] = volume if volume > 0 else 0
                slot += 1

    newDf = dfToNotes.to_dict('records')
    newDfHit  = [deepcopy(n) for n in newDf if math.isnan(n['length'])]
    newDfHold = [deepcopy(n) for n in newDf if not math.isnan(n['length'])]
    for n in newDfHit:
        del n['length']
    mToCopy.notes = OsuNotePkg(hits=OsuHitList([OsuHitObj(**hit) for hit in newDfHit]),
                               holds=OsuHoldList([OsuHoldObj(**hold) for hold in newDfHold]))

    return None if inplace else mToCopy
