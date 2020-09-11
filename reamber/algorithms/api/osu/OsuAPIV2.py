from __future__ import annotations
import requests
from dataclasses import dataclass
from configparser import ConfigParser

BASE_URL = "https://osu.ppy.sh/api/v2"

@dataclass
class OsuAPIV2:
    """ This class helps in connecting with the new osu! API.

    This isn't fleshed out yet since a lot of useful functionality is not implemented yet.
    """
    token: str

    @staticmethod
    def fromPost(secret=None, id_=None, cfg_path="") -> OsuAPIV2:
        """ This grabs the token by requesting a new one with the secret and id """
        if not (secret and id_):
            if not cfg_path:
                raise TypeError("Secret and ID or cfg_path must be defined.")
            else:  # cfg_path is given
                cfg = ConfigParser()
                cfg.read(cfg_path, encoding='utf-8')
                id_ = cfg['API']['id']
                secret = cfg['API']['secret']

        response = requests.post("https://osu.ppy.sh/oauth/token",
                           data={"client_id": id_,
                                 "client_secret": secret,
                                 "grant_type": "client_credentials",
                                 "scope": "public"})

        payload = eval(response.text)
        return OsuAPIV2(payload['access_token'])

    @staticmethod
    def fromCfg(cfg_path):
        """ This grabs the token from the current cfg, good if you don't want to keep on requesting tokens

        However note that the token will expire in 24 hours upon request."""

        cfg = ConfigParser()
        cfg.read(cfg_path, encoding='utf-8')
        return OsuAPIV2(cfg['API']['token'])

    def get(self, api_path, **kwargs):
        return requests.get(f"{BASE_URL}{api_path}",
                            params={k: v for k, v in kwargs.items() if v},
                            headers={"Authorization": f"Bearer {self.token}"})

    def beatmapScores(self, id_):
        return self.get(f"/beatmaps/{id_}/scores")

    def beatmap(self, id_):
        return self.get(f"/beatmaps/{id_}")

    def beatmapSet(self, id_):
        return self.get(f"/beatmapsets/{id_}")

    def userKudosu(self, id_, limit=None, offset=None):
        return self.get(f"/users/{id_}/kudosu", limit=limit, offset=offset)

    def _userScores(self, id_, type_, includeFails, mode, limit, offset):
        return self.get(f"/users/{id_}/scores/{type_}",
                        includeFails=includeFails, mode=mode, limit=limit, offset=offset)

    def userScoresBest(self, id_, includeFails=None, mode=None, limit=None, offset=None):
        return self._userScores(id_, type_="best",
                        includeFails=includeFails, mode=mode, limit=limit, offset=offset)

    def userScoresFirsts(self, id_, includeFails=None, mode=None, limit=None, offset=None):
        return self._userScores(id_, type_="firsts",
                        includeFails=includeFails, mode=mode, limit=limit, offset=offset)

    def userScoresRecent(self, id_, includeFails=None, mode=None, limit=None, offset=None):
        return self._userScores(id_, type_="recent",
                        includeFails=includeFails, mode=mode, limit=limit, offset=offset)
