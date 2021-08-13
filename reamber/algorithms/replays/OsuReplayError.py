from dataclasses import dataclass
from typing import List, Union, Tuple

from osrparse import parse_replay_file, Replay, Mod, ReplayEventMania
from reamber.osu.OsuMap import OsuMap

@dataclass
class ManiaHitErrorEvents:
    """ The events of the errors

    hit_errors are the press errors (including LN head)
    rel_errors are the release errors (only LN tail)

    _map prefix means the map metrics
    _reps prefix means the replay metrics
    """

    hit_errors: List[List[List[int]]]
    rel_errors: List[List[List[int]]]
    hit_map:    List[List[int]]
    rel_map:    List[List[int]]
    ln_len_map: List[List[int]]
    hit_reps:   List[List[List[int]]]
    rel_reps:   List[List[List[int]]]

class OsuReplayError:
    """Finds the errors in osu! replays.

    Note the different conventions:
    Hit: Press Key
    Rel/Release: Release Key

    For each key, there are Hit and Rel errors.
    """

    reps: Union[List[Replay], Replay]
    map: OsuMap
    keys: int
    judge: dict

    def __init__(self,
                 reps: Union[List[str], str, List[Replay], Replay],
                 map: Union[OsuMap, str]):
        """ Initialize with replay paths, map paths or Replay and OsuMap

        If you want to initialize the Replays or OsuMap, use the respective classes.

        Replays can be generated with parse_replay_file from osrparse.

        :param reps: Can be a list of Replays or replay paths.
        :param map: Can be an OsuMap or a path to OsuMap.
        """

        # Cast to list if not list
        self.reps = reps if isinstance(reps, list) else [reps]
        self.reps = [parse_replay_file(r) if isinstance(r, str) else r for r in self.reps]

        self.map = map if isinstance(map, OsuMap) else OsuMap.read_file(map)
        self.keys = int(self.map.circle_size)
        OD = self.map.overall_difficulty
        self.judge = dict(
            J300G=16,
            J300=64 - 3 * OD,
            J200=97 - 3 * OD,
            J100=127 - 3 * OD,
            J50=151 - 3 * OD,
            JMISS=188 - 3 * OD,
        )

    def errors(self) -> ManiaHitErrorEvents:
        """ Parses Both replay and map and calculates their errors.

        :return ManiaHitErrorEvents(hit_error=hit_error,
                                    rel_error=rel_error,
                                    hit_map=hit_map,
                                    rel_map=rel_map,
                                    hit_reps=hit_reps,
                                    rel_reps=rel_reps)
        """
        hit_rep, rel_rep = self._parse_replays()
        hit_map, rel_map, ln_len_map = self._parse_map(self.map)
        return self._sync(hit_map, rel_map, ln_len_map, hit_rep, rel_rep)

    def _parse_replays(self) -> Tuple[List[List[List[int]]], List[List[List[int]]]]:
        """ Parses the map and returns the list of hit and release locations

        Returns Hit[Replay][Key][Offsets], Rel[Replay][Key][Offsets]

        :return rep_hit, rep_rel
        """
        hit_reps = []
        rel_reps = []
        for rep in self.reps:
            assert isinstance(rep, Replay), f"Received reps is not of Replay. {type(rep)}"
            rep_data = rep.play_data

            # Reformat data from relative offsets to absolute.
            prev = 0
            t = 0
            rep_events = []
            for d in rep_data:
                d: ReplayEventMania
                t += d.time_delta
                if prev != d.keys:
                    rep_events.append((t, int(d.keys)))
                prev = d.keys

            # Reformat hits and rels to individual actions
            hit_rep = [[] for _ in range(self.keys)]
            rel_rep = [[] for _ in range(self.keys)]
            status = [False] * self.keys
            for ev in rep_events:

                offset = ev[0]
                keys = ev[1]

                if offset < 0: continue  # Ignore key presses < 0ms

                for k in range(self.keys):
                    if keys & (2 ** k) != 0 and not status[k]:
                        # k is pressed and wasn't pressed before
                        hit_rep[k].append(offset)
                        # Update status to pressed
                        status[k] = True
                    elif status[k] and keys & (2 ** k) == 0:
                        # k is not pressed and was pressed before
                        rel_rep[k].append(offset)
                        # Update status to released
                        status[k] = False

            if rep.mod_combination & Mod.Mirror:
                hit_reps.append(list(reversed(hit_rep)))
                rel_reps.append(list(reversed(rel_rep)))
            else:
                hit_reps.append(hit_rep)
                rel_reps.append(rel_rep)

        return hit_reps, rel_reps

    @staticmethod
    def _parse_map(map: OsuMap):
        """ Parses the map and returns the list of hit and release locations

        :return: map_hit, map_rel
        """
        hit_map_ = [*[(h.offset, h.column) for h in map.hits],
                    *[(h.offset, h.column) for h in map.holds]]
        rel_map_    = [(int(h.tail_offset), h.column) for h in map.holds]
        ln_len_map_ = [(int(h.length), h.column) for h in map.holds]

        hit_map = [[] for _ in range(int(map.circle_size))]
        for h in hit_map_:
            hit_map[h[1]].append(h[0])

        rel_map = [[] for _ in range(int(map.circle_size))]
        for h in rel_map_:
            # noinspection PyTypeChecker
            rel_map[h[1]].append(h[0])

        ln_len_map = [[] for _ in range(int(map.circle_size))]
        for h in ln_len_map_:
            # noinspection PyTypeChecker
            ln_len_map[h[1]].append(h[0])

        hit_map    = [sorted(i) for i in hit_map]
        rel_map    = [sorted(i) for i in rel_map]
        ln_len_map = [sorted(i) for i in ln_len_map]

        return hit_map, rel_map, ln_len_map

    def _sync(self,
              hit_map: List[List[int]],
              rel_map: List[List[int]],
              ln_len_map: List[List[int]],
              hit_reps: List[List[List[int]]],
              rel_reps: List[List[List[int]]],
              ) -> ManiaHitErrorEvents:
        hit_errors, rel_errors = self._find_error(
            hit_map=hit_map, rel_map=rel_map, hit_reps=hit_reps, rel_reps=rel_reps)
        return ManiaHitErrorEvents(hit_errors=hit_errors,
                                   rel_errors=rel_errors,
                                   hit_map=hit_map,
                                   rel_map=rel_map,
                                   hit_reps=hit_reps,
                                   rel_reps=rel_reps,
                                   ln_len_map=ln_len_map)

    def _find_error(self,
                    hit_map: List[List[int]],
                    rel_map: List[List[int]],
                    hit_reps: List[List[List[int]]],
                    rel_reps: List[List[List[int]]]):
        """ This finds the error of the plays via simulation.

        Note that releases may not sync correctly via naive simulation. That means, a
        release of a normal note may be detected early as release for an LN if it's
        too close.

        """
        # errors is for ALL REPLAYS
        hit_errors = []
        rel_errors = []
        for hit_rep, rel_rep in zip(hit_reps, rel_reps):
            # error is for A SINGLE REPLAY
            error = [[] for _ in range(self.keys)]
            for k in range(self.keys):
                # True for is Release
                hit_map_k = [(i, False) for i in hit_map[k]]
                rel_map_k = [(i, True) for i in rel_map[k]]
                hit_rep_k = [(i, False) for i in hit_rep[k]]
                rel_rep_k = [(i, True) for i in rel_rep[k]]

                map_k = sorted([*hit_map_k, *rel_map_k], key=lambda x: x[0])
                rep_k = sorted([*hit_rep_k, *rel_rep_k], key=lambda x: x[0])

                map_i = 0
                rep_i = 0

                while True:
                    if map_i >= len(map_k):
                        # map is complete
                        break
                    elif rep_i >= len(rep_k):
                        # replay is complete
                        # If map isn't complete, we need to pad it with the missing hits
                        # This occurs if the player just doesn't hit the last few notes.
                        for i in range(map_i, len(map_k)):
                            error[k].append((self.judge['JMISS'], map_k[i][1]))
                        break

                    map_offset, map_rel = map_k[map_i]
                    rep_offset, rep_rel = rep_k[rep_i]

                    # Release Condition
                    # REP MAP
                    #  X   X  Normal
                    #  O   X  +REP
                    #  X   O  +REP
                    #  O   O  Release

                    if rep_rel != map_rel:
                        # REP REL MAP HIT
                        # Release happened while no LNs are present
                        # E.g.
                        #  [ ]       [ ]=======[ ]
                        #   ^    ^              |
                        #  HIT  REL<------------+
                        #  The release shouldn't interact with the next LN if it's too short

                        # REP HIT MAP REL
                        # Hit happened during LNs
                        # E.g.
                        #  [ ]=======[ ]       [ ]
                        #   ^    ^              |
                        # Probably an accidental press, just ignore it
                        rep_i += 1
                        continue

                    if rep_offset < map_offset - self.judge['JMISS']:
                        # Early No Hit
                        rep_i += 1
                        # if self.debug: self. _print_status("--", k, rep_offset, map_offset)
                    elif map_offset - self.judge['JMISS'] <= rep_offset < map_offset - self.judge['J50']:
                        # Early Miss
                        map_i += 1
                        rep_i += 1
                        # If this is a release, we half the prior error and the current
                        # This is how LNs in osu! work
                        if map_rel:
                            error[k][-1][0] /= 2
                            error[k].append([(rep_offset - map_offset) / 2, map_rel])
                        else:
                            error[k].append([rep_offset - map_offset, map_rel])
                        # if self.debug: self._print_status("EM", k, rep_offset, map_offset)
                    elif map_offset - self.judge['J50'] <= rep_offset < map_offset + self.judge['JMISS']:
                        # Not too sure if we have Late Misses
                        # Valid Hit
                        map_i += 1
                        rep_i += 1
                        # If this is a release, we half the prior error and the current
                        # This is how LNs in osu! work
                        if map_rel:
                            error[k][-1][0] /= 2
                            error[k].append([(rep_offset - map_offset) / 2, map_rel])
                        else:
                            error[k].append([rep_offset - map_offset, map_rel])
                        # if self.debug: self._print_status("OK", k, rep_offset, map_offset)
                    elif rep_offset >= map_offset + self.judge['JMISS']:
                        # Late No Hit
                        map_i += 1
                        error[k].append([self.judge['JMISS'], map_rel])
                        # if self.debug: self._print_status("--", k, rep_offset, map_offset)
                    else:
                        raise Exception(f"{map_offset} unmatched with {rep_offset}")
            hit_errors.append([[e[0] for e in k if not e[1]] for k in error])
            rel_errors.append([[e[0] for e in k if e[1]] for k in error])
        return hit_errors, rel_errors

    @staticmethod
    def _print_status(status, col, hit, note):
        print(f"{status}, COL: {col}, Error: {hit - note:<5}, Hit: {hit:<6}, Note: {note:<6}")
