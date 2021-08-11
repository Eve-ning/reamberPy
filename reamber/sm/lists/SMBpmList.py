from __future__ import annotations

from reamber.base.Property import list_props
from reamber.base.lists.BpmList import BpmList
from reamber.sm import SMBpm


@list_props(SMBpm)
class SMBpmList(BpmList[SMBpm]):

    # TODO: Important thing to fix if we want correct snaps.
    #  Will have to dynamically create bpm slots to avoid weird bpms
    def reseat(self, item_class=SMBpm):
        """ Force Reseats the BPM List such that metronomes are always 4. """
        bpms = super().reseat(item_class)
        bpms.bpm /= bpms.metronome / SMBpm.DEFAULT_BEATS_PER_MEASURE
        bpms.metronome = 4.0
        return bpms

