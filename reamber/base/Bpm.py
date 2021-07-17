from __future__ import annotations

from typing import List, Tuple, Union

from reamber.base.Property import item_props
from reamber.base.RAConst import RAConst
from reamber.base.Timed import Timed


@item_props()
class Bpm(Timed):
    """ A non-playable timed object that specifies the tempo of the map.

    This is synonymous with Bpm Point, it's named Object to make it consistent
    """

    _props = dict(bpm='float',
                  metronome='float')

    def __init__(self, offset: float, bpm: float, metronome: int = 4, **kwargs):
        super().__init__(offset=offset, bpm=bpm, metronome=metronome, **kwargs)

    @property
    def beat_length(self) -> float:
        """ Returns the length of the beat in ms """
        return RAConst.min_to_msec(1.0 / self.bpm)

    @property
    def metronome_length(self) -> float:
        """ Returns the length of the metronome in ms """
        return self.beat_length * self.metronome

    def beat(self, bpms: List[Bpm]):
        """ Gets the beat of the current BPM Point w.r.t. bpms """
        return Bpm.get_beats([self.offset], bpms)[0]

    @staticmethod
    def snap_exact(offsets: List[float], bpms: List[Bpm], snap_precision: int = 64):
        """ Snaps the offsets to the exact snap

        Returns in the exact same order.

        Example::

            Bpm.snapExact([1, 100, 250, 385], bpms=[Bpm(0, 150)], snapPrecision=16)
            [400.0, 300.0, 100.0, 0.0]

        :param offsets: The offsets to snap
        :param bpms: The full list of BPMs
        :param snap_precision: The precision of snapping, 1 = 1/1 (4ths), 8 = 1/8 (32nds), ...
        :return:

        """
        offsets_sort = sorted(offsets, reverse=True)
        offsets_index = [offsets.index(x) for x in offsets_sort]

        bpm_i = 0
        # noinspection PyTypeChecker
        bpms_sorted = sorted(bpms, reverse=True)
        offsets_out = []

        for offset in offsets_sort:
            try:
                while offset < bpms_sorted[bpm_i].offset:
                    bpm_i += 1
            except IndexError:
                raise IndexError("Offset located before first BPM")
            snap_length = RAConst.min_to_msec(4 / (snap_precision * bpms_sorted[bpm_i].bpm))
            error = (offset - bpms_sorted[bpm_i].offset) % snap_length
            if error < snap_length / 2: offsets_out.append(offset - error)
            else:                      offsets_out.append(offset + (snap_length - error))

        # This returns the offsets sorted as the original
        return [x for _,x  in sorted(zip(offsets_index, offsets_out), key=lambda x: x[0])]

    # Beats are used for the StepMania format
    # One large caveat for beats is that it requires looping through the BPM Points of the map to
    # calculate 1 single beat
    # Hence There is a getBeats and getBeat, where if getBeats is used for a list instead of looping through
    # getBeat, it'll be marginally faster.

    @staticmethod
    def get_beats(offsets: Union[List[float], List[Timed], float],
                  bpms: List[Bpm]) -> List[float]:
        """ Gets the beat numbers from offsets provided, this is relative to the first Timing Point

        :param offsets: Offsets to find beat from, can be a list of TOs or floats or a single float
        :param bpms: The Global BPM list
        :return: Beat numbers with respect to the first Timing Point provided.
        """
        # The idea here is to loop through the BPM Points once while filling the beats list with the correct offsets
        # 1.  For each offset:
        # 1.1 Go through the bpms until we find the 2 BPMs that sandwich it
        #     [BPM] [Offset] [BPM]
        # 1.2 If the offset cannot be sandwiched, then we use the last bpm to reference
        #     [BPM] [Offset]
        #
        # 2.  While we are looping through BPMs to find, we need to take note of the prior Beat
        # 2.1 For each BPM iteration, we update bpm_prev_beat
        #
        # 3.  Once we found the sandwich, we find the difference in offsets and find out the beat of the offset

        # Main problem obviously is if the offsets or bpms are not sorted, it'll break the algorithm
        # So we need to get a sorted offset and sorted bpm
        # Unfortunately, unless we force implement sorting on the higher level,
        # this sorting algorithm will have to stay

        # Firstly, coerce the offsets into a List[float] if it's not already
        offsets_ = offsets if isinstance(offsets, List) else [offsets]
        offsets_: Union[List[Timed], List[float]]
        if len(offsets_) == 0: return []
        offsets_ = [x.offset for x in offsets_] if isinstance(offsets_[0], Timed) else offsets_
        offsets_: List[float]

        # We attach an enum to the original list and sort by the offsets, this sorts it once
        # noinspection PyTypeChecker
        offsets_sorted_: List[Tuple[int, float]] = [x for x in sorted(enumerate(offsets_), key=lambda x:x[1])]
        offsets_sorted_order: List[int]  # This is the original order
        offsets_sorted: List[float]
        offsets_sorted_order, offsets_sorted = zip(*offsets_sorted_)  # Unpacks into the original order and sort

        del offsets_sorted_, offsets_

        bpm_index = 0
        bpm_prev_beat = 0  # If we skip TPs, we have to account for their previous beat

        beats: List[float] = []
        bpms.sort()

        for offset in offsets_sorted:
            # Shift TP such that tp is the latest
            while bpm_index != len(bpms) - 1 and \
                    not (bpms[bpm_index].offset <= offset < bpms[bpm_index + 1].offset):
                bpm_index += 1
                bpm_prev_beat += (bpms[bpm_index].offset - bpms[bpm_index - 1].offset) /\
                                bpms[bpm_index - 1].beat_length

            beats.append(bpm_prev_beat + ((offset - bpms[bpm_index].offset) / bpms[bpm_index].beat_length))

        # Sorts beats by original order
        return [x for x, _ in sorted(zip(beats, offsets_sorted_order), key=lambda x:x[1])]

    @staticmethod
    def align_bpms(bpms: List[Bpm],
                   BEAT_ERROR_THRESHOLD: float = 0.001,
                   BEAT_CORRECTION_FACTOR: float = 5.0) -> List[Bpm]:
        """ Ensures that all BPMs are on an integer measure by adding or amending

        :param bpms: The BPMs
        :param BEAT_ERROR_THRESHOLD: If the fraction change in beat's is more than this, we append a new BPM, else we \
            create a new bpm. i.e. if there's too many high BPM points, then increase this
        :param BEAT_CORRECTION_FACTOR: The number of beats to search prior to the affected beat to amend. i.e. if \
            there are too many incorrectly snapped notes DUE TO ADDED BPMs then decrease this
        :return: The new and old BPMs
        """
        # Summary
        # We ensure that all BPMs are on an integer measure, this makes it such that it's easier to snap

        # This will be a conditional of alignBpms
        # If the BPM is misaligned to a measure
        #   If there is a BPM less than or equal to a beat prior
        #       Adjust that one
        #   Else
        #       Create a BPM 1 Beat prior

        # Edge cases
        # Sometimes the beat is like X.000001
        # For this, we wouldn't want to add a BPM at X and shift this to X+1
        # This is because we'll get a very high BPM here and it'll look ugly
        # For this, we will add a BPM at X-1 or amend X-1.

        # Hence
        # If X.000        : Don't change anything
        # If Amend        : Just amend the previous
        # If X.000 ~ X.001: Change X-1
        # If X.001 ~ X.999: Change X   & Move to X + 1
        # BEAT_ERROR_THRESHOLD

        # The beat correction factor defines how many beats to look behind to correct a bpm point
        # BEAT_CORRECTION_FACTOR

        bpm_beats = Bpm.get_beats(bpms, bpms)
        bpms_new: List[Bpm] = [bpms[0]]
        for bpm_index in range(1, len(bpms)):  # Note We don't touch the first bpm, that's assumed to be 0.0
            bpm_prev = bpms[bpm_index - 1]
            bpm_curr = bpms[bpm_index]
            bpm_beat_prev = bpm_beats[bpm_index - 1]
            bpm_beat_curr = bpm_beats[bpm_index]

            bpm_beat_error = (bpm_beat_curr - bpm_beat_prev) % 1.0

            if bpm_beat_error == 0.0:
                pass
            elif bpm_curr.offset - bpm_curr.beat_length * BEAT_CORRECTION_FACTOR <= bpm_prev.offset <= bpm_curr.offset:
                # This is the case when the previous BPM is within (1 * BCF) beats of the current BPM
                # Instead of inserting another BPM, we amend the previous BPM
                bpms_new[-1].bpm = 1 / RAConst.msec_to_min(bpm_curr.offset - bpm_prev.offset)
            elif bpm_beat_error < BEAT_ERROR_THRESHOLD:
                # As defined, if we happen to have an error that's less than the threshold, instead of forcing
                # a new bpm, we amend the prior bpm OR add a bpm point 1 beat before
                bpms_new.append(Bpm(offset=bpm_curr.offset - (1.0 + bpm_beat_error) * bpm_prev.beat_length,
                                    bpm=1.0 / RAConst.msec_to_min(bpm_prev.beat_length * (1 + bpm_beat_error))))
            else:
                # This is the case when the beat is significant enough that it warrants a BPM point in its place
                bpms_new.append(Bpm(offset=bpm_curr.offset - bpm_beat_error * bpm_prev.beat_length,
                                    bpm=1.0 / RAConst.msec_to_min(bpm_prev.beat_length * bpm_beat_error)))

            bpms_new.append(bpm_curr)

        return bpms_new

