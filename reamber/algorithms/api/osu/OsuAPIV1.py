from __future__ import annotations
import requests
from dataclasses import dataclass
from configparser import ConfigParser
from enum import Enum

BASE_URL = "https://osu.ppy.sh/api"

@dataclass
class OsuAPIV1:

    key: str

    @staticmethod
    def from_cfg(cfg_path):
        """ This loads the key given in the cfg """

        cfg = ConfigParser()
        cfg.read(cfg_path, encoding='utf-8')
        return OsuAPIV1(cfg['API']['key'])

    def get(self, api_path, **kwargs):
        """ Sends a GET request to path specified, with kwargs as params.

        Implicitly, key is sent in the params too.

        :param api_path: The path, including first forward slash
        :param kwargs: Other params to send with the request
        """
        return requests.get(f"{BASE_URL}{api_path}",
                            params={**{k: str(v) for k, v in kwargs.items() if v},
                                    "k": self.key})

    def _drop_self(self, lcls: dict):
        """ Drops the self key from the dictionary, helper function"""
        return {k: v for k, v in lcls.items() if k != "self"}

    def get_beatmaps(self, since=None, s=None, b=None, u=None, type=None, m=None, a=None, h=None, limit=None, mods=None):
        """ Gets beatmaps.

        :param since: return all beatmaps ranked or loved since this date. Must be a MySQL date. In UTC
        :param s: Beatmapset_id
        :param b: Beatmap_id
        :param u: User_id or a username
        :param type: specify if u is a user_id or a username. Use string for usernames or id for user_ids.
        :param m: Mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania).
        :param a: Include converted beatmaps (0 = not included, 1 = included).
        :param h: The beatmap hash.
        :param limit: Amount of results. Default and maximum are 500.
        :param mods: Beatmap Mods
        """

        return self.get(f"/get_beatmaps", **self._drop_self(locals()))

    def get_user(self, u, m=None, type=None, event_days=None):
        """ Gets stats about user

        :param u: User_id or a username
        :param m: Mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania).
        :param type: specify if u is a user_id or a username. Use string for usernames or id for user_ids.
        :param event_days: Max number of days between now and last event date. Range of 1-31. Default value is 1.
        """
        return self.get(f"/get_user", **self._drop_self(locals()))

    def get_user_best(self, u, m=None, limit=None, type=None):
        """ Get Best scores

        :param u: User_id or a username
        :param m: Mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania).
        :param limit: Amount of results. Default 10, max 100
        :param type: specify if u is a user_id or a username. Use string for usernames or id for user_ids.
        """
        return self.get(f"/get_user_best", **self._drop_self(locals()))

    def get_user_recent(self, u, m=None, limit=None, type=None):
        """ Get Recent scores

        :param u: User_id or a username
        :param m: Mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania).
        :param limit: Amount of results. Default 10, max 100
        :param type: specify if u is a user_id or a username. Use string for usernames or id for user_ids.
        """
        return self.get(f"/get_user_recent", **self._drop_self(locals()))

    def get_match(self, mp):
        """ Gets details about match

        :param mp: Match ID
        """
        return self.get(f"/get_match", **self._drop_self(locals()))

    def get_replay(self, b, u, m=None, s=None, type=None, mods=None):
        """ Gets a single replay

        :param b: Beatmap_id
        :param u: User_id or a username
        :param m: Mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania).
        :param s: specify a score id to retrieve the replay data for. May be passed instead of b and u.
        :param type: specify if u is a user_id or a username. Use string for usernames or id for user_ids.
        :param mods: Beatmap Mods
        """
        return self.get(f"/get_replay", **self._drop_self(locals()))

    def get_scores(self, b, u=None, m=None, mods=None, type=None, limit=None):
        """ Gets scores from beatmap

        :param b: Beatmap_id
        :param u: User_id or a username
        :param m: Mode (0 = osu!, 1 = Taiko, 2 = CtB, 3 = osu!mania).
        :param mods: Beatmap Mods
        :param type: specify if u is a user_id or a username. Use string for usernames or id for user_ids.
        :param limit: Amount of results. Default 50, max 100
        """
        return self.get(f"/get_scores", **self._drop_self(locals()))

    class MODE(Enum):
        STANDARD = 0
        TAIKO = 1
        CATCH = 2
        MANIA = 3

    class MOD(Enum):
        NONE        = 0
        NOFAIL      = 1
        EASY        = 2
        TOUCHDEVICE = 4
        HIDDEN      = 8
        HARDROCK    = 16
        SUDDENDEATH = 32
        DOUBLETIME  = 64
        RELAX       = 128
        HALFTIME    = 256
        NIGHTCORE   = 512
        FLASHLIGHT  = 1024
        AUTOPLAY    = 2048
        SPUNOUT     = 4096
        RELAX2      = 8192
        PERFECT     = 16384
        KEY4        = 32768
        KEY5        = 65536
        KEY6        = 131072
        KEY7        = 262144
        KEY8        = 524288
        FADEIN      = 1048576
        RANDOM      = 2097152
        CINEMA      = 4194304
        TARGET      = 8388608
        KEY9        = 16777216
        KEYCOOP     = 33554432
        KEY1        = 67108864
        KEY3        = 134217728
        KEY2        = 268435456
        SCOREV2     = 536870912
        MIRROR      = 1073741824
