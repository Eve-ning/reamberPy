from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, DefaultDict

import numpy as np
from osrparse import Replay, Mod, ReplayEventMania, parse_replay_file

from reamber.osu.OsuMap import OsuMap


class Offsets(List[float]):
    ...


class ActionOffsets(DefaultDict[int, Offsets]):
    def __init__(self, *args, **kwargs):
        super(ActionOffsets, self).__init__(*args, **kwargs)
        self.default_factory = Offsets


@dataclass
class ReplayOffsets:
    hits: ActionOffsets = field(default_factory=ActionOffsets)
    releases: ActionOffsets = field(default_factory=ActionOffsets)


@dataclass
class ManiaHitErrorEvents:
    """ The events of the errors """

    errors: ReplayOffsets
    map_offsets: ReplayOffsets
    rep_offsets: ReplayOffsets


class OsuReplayError:
    """ Finds the errors in osu! replays.

    Notes:
        Hit: Press Key
        Rel/Release: Release Key

        For each key, there are Hit and Rel errors.
    """

    reps: List[Replay] | Replay
    map: OsuMap
    keys: int
    judge: dict

    def __init__(self,
                 reps: List[str] | str | List[Replay] | Replay,
                 map: OsuMap | str):
        """ Initialize with replay paths, map paths or Replay and OsuMap

        Replays can be generated with parse_replay_file from osrparse.

        Args:
            reps: Can be a list of Replays or replay paths.
            map: Can be an OsuMap or a path to OsuMap.
        """

        # Cast to list if not list
        self.reps = reps if isinstance(reps, list) else [reps]
        self.reps = [
            parse_replay_file(r)
            if isinstance(r, str)
            else r for r in self.reps
        ]

        self.map = map if isinstance(map, OsuMap) else OsuMap.read_file(map)
        self.keys = int(self.map.circle_size)
        od = self.map.overall_difficulty
        self.judge = dict(J300G=16,
                          J300=64 - 3 * od,
                          J200=97 - 3 * od,
                          J100=127 - 3 * od,
                          J50=151 - 3 * od,
                          JMISS=188 - 3 * od)

    def errors(self) -> ManiaHitErrorEvents:
        """ Parses replay errors as ManiaHitErrorEvents """
        rep_offsets = self.parse_replays()
        map_offsets = self.parse_map()

        errors = ReplayOffsets()
        for k in range(self.keys):
            for m, r, e in zip(
                (map_offsets.hits, map_offsets.releases),
                (rep_offsets.hits, rep_offsets.releases),
                (errors.hits, errors.releases)
            ):
                m = np.array(m[k])
                r = np.array(r[k])

                diff = m[:, np.newaxis] - r
                e[k] = diff[np.arange(diff.shape[0]),
                            np.argmin(np.abs(diff), axis=1)]

        return ManiaHitErrorEvents(errors, map_offsets, rep_offsets)

    def parse_map(self) -> ReplayOffsets:
        hits = ActionOffsets()
        rels = ActionOffsets()
        s = self.map.stack()
        for k in range(self.keys):
            s_key = s.loc[s.column == k]
            hits[k] = s_key['offset'].tolist()
            rels[k] = (s_key['offset'] + s_key['length']).dropna().tolist()
        return ReplayOffsets(hits, rels)

    def parse_replays(self) -> ReplayOffsets:
        """ Parses the map and returns the list of hit and release locations

        Returns Hit[Replay][Key][Offsets], Rel[Replay][Key][Offsets]

        Returns:
            rep_hit, rep_rel
        """
        rep_offsets = ReplayOffsets()
        for rep in self.reps:
            if not isinstance(rep, Replay):
                raise ValueError(f"Received reps isn't of Replay. {type(rep)}")

            # Reformat data from relative offsets to absolute.
            t = 0
            rep_evs = []

            prev_key_bits = 0
            for rep_ev in rep.play_data:
                rep_ev: ReplayEventMania
                key_bits = rep_ev.keys
                t += rep_ev.time_delta
                if prev_key_bits != key_bits:
                    rep_evs.append((t, int(key_bits)))
                prev_key_bits = key_bits

            # Reformat hits and rels to individual actions
            hits = ActionOffsets()
            rels = ActionOffsets()
            status = [False] * self.keys

            for offset, key_bits in rep_evs:
                if offset < 0: continue  # Ignore key presses < 0ms

                for k in range(self.keys):
                    if (key_bits >> k) & 1 != 0 and not status[k]:
                        # k is pressed and wasn't pressed before
                        hits[k].append(offset)
                        # Update status to pressed
                        status[k] = True
                    elif (key_bits >> k) & 1 == 0 and status[k]:
                        # k is not pressed and was pressed before
                        rels[k].append(offset)
                        # Update status to released
                        status[k] = False

            if rep.mod_combination & Mod.Mirror:
                rep_offsets.hits = list(reversed(hits))
                rep_offsets.releases = list(reversed(rels))
            else:
                rep_offsets.hits = hits
                rep_offsets.releases = rels

        return rep_offsets
