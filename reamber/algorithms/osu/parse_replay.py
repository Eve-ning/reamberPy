from __future__ import annotations

from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
from osrparse import Replay, parse_replay_data, GameMode
from tqdm import tqdm

from reamber.osu import OsuMap

DataSource = Literal["api", "file", "infer"]


def parse_replay_actions(
        replay: str | Path,
        *,
        keys: int,
        src: DataSource = "infer"
) -> pd.DataFrame:
    """ Parses replays into actions in a DataFrame

    Notes:
        This will use osrparse to read the files/api data.

        The source inference checks if ``replay`` ends with ``.osu``.

    Examples:

        From .osr file::

            >>> parse_replay_actions("path/to.osr", src="file", keys=7)

        From osu! API::

            >>> import requests
            >>> url = f'https://osu.ppy.sh/api/get_replay?k={api_key}&s={score_id}&m=3'
            >>> response = requests.get(url)
            >>> parse_replay_actions(response.json()['content'], src='api', keys=4)

        From a .osr file, with inferred source::

            >>> parse_replay_actions("path/to.osr", keys=7)

    Args:
        replay: Replay path OR response content from v1 get_replay/ API
        src: Must be "api", "file", indicating the source of the data or "infer" to automatically infer the source
        keys: Number of keys of the map associated with the replay

    Returns:
        A long dataframe indicating the actions of the replay.

        - offset (int): ms offset of the action
        - column (int): column associated with the action
        - is_press (bool): whether the action is to press or release.
    """
    if src == "infer":
        src = "file" if str(replay).endswith(".osr") else "api"
    r = Replay.from_path(replay).replay_data if src == "file" else parse_replay_data(replay, mode=GameMode.MANIA)

    df = pd.DataFrame(r).rename({"time_delta": "delta", "keys": "state"}, axis=1)
    df = df.loc[df.delta != 0]

    df_long_state = (
        # Parse the offset from our delta
        df.assign(offset=df.delta.cumsum().astype(int))
        # Drop unused delta
        .drop('delta', axis=1)
        # Mask out useless data
        .loc[df.state.diff().fillna(0) != 0]
        # cast state to int
        .astype(dict(state=int))
        # Format each state into a fixed length binary
        .assign(
            # The binary string is flipped, we need to [::-1]
            state=lambda x: x.state.apply(lambda i: list(f"{i:0{keys}b}"[::-1]))
        )
    )

    # We create another dataframe with exploded columns with respective bits
    # indicating the state
    df_wide_state = pd.DataFrame(
        df_long_state.state.tolist(),
        columns=range(keys),
        index=df_long_state['offset']
    ).astype(int)

    # We find the changes in states, which leads us to the actions
    df_action = (
        df_wide_state
        # The difference in states will yield {1, -1}, indicating action
        #  1: State Off -> On <=> Press
        # -1: State On -> Off <=> Release
        .diff()
        # Drop the NaN created by diff on first entry
        .dropna()
        # Melt all columns into a long table
        .melt(var_name='column', value_name='is_press', ignore_index=False)
        # Remove all non-actions
        .loc[lambda x: x.is_press != 0]
        # Make is_press a boolean
        .assign(is_press=lambda x: x.is_press == 1)
        # Pull offset out of index
        .reset_index()
    )

    return df_action


def parse_replays_error(
        replays: dict[object, str | Path],
        osu: OsuMap,
        *,
        src: DataSource = "infer",
        verbose: bool = True
):
    """ Parses replays as replay errors w.r.t. the map using minimum absolute distance matching.

    See Also:
        ``parse_replay_actions``

    Notes:
        This replay error parsing is not exact to errors simulated by the osu! engine as it uses a naive minimum
        absolute distance matching. The calculated error is less accurate for dense maps.

        ``keys`` is automatically inferred from the ``osu`` map.

    Examples:

        From .osr files::

            >>> er = parse_replays_error(
            >>>     replays={"rep1": Path("path/to1.osr"),
            >>>              "rep2": Path("path/to2.osr")},
            >>>     osu=OsuMap.read_file("path/to.osu"),
            >>>     src="file"
            >>> )

        From osu! API::

            >>> import requests
            >>> url1 = f'https://osu.ppy.sh/api/get_replay?k={api_key}&s={score_id1}&m=3'
            >>> response1 = requests.get(url1)
            >>> url2 = f'https://osu.ppy.sh/api/get_replay?k={api_key}&s={score_id2}&m=3'
            >>> response2 = requests.get(url2)
            >>> er = parse_replays_error(
            >>>     replays={"rep1": response1.json()['content'],
            >>>              "rep2": response2.json()['content']},
            >>>     osu=OsuMap.read_file("path/to.osu"),
            >>>     src="api"
            >>> )

        Note that you can mix sources with "infer", as long as inferring is correct.
        See how ``parse_replay_actions`` infer sources.

    Args:
        replays: A dictionary of key: id, value: replays paths OR response contents from v1 get_replay/ API.
        osu: Map to reference errors from
        src: Must be "api", "file", indicating the source of the data or "infer" to automatically infer the source
        verbose: Whether to turn off the progress bar

    Returns:
        A long dataframe of the replay error.

        - Index replay_id (object): identifier from ``replays.keys()``
        - offset (int): ms offset of the action
        - column (int): column associated with the action
        - is_press (bool): whether the action is to press or release.
        - error (int): the estimated error of the action
    """

    def get_error(ar_map_offsets: np.ndarray, ar_rep_offsets: np.ndarray):
        # Get difference matrix
        ar_delta = ar_map_offsets - ar_rep_offsets[:, np.newaxis]
        # Find indexes where abs differences is minimum
        ar_delta_argmin = np.argmin(np.abs(ar_delta), axis=0)
        # Retrieve those entries
        return ar_delta[ar_delta_argmin, np.arange(ar_delta.shape[1])]

    dfs_error = []
    keys = int(osu.circle_size)
    dfs_action = [parse_replay_actions(replay=replay, src=src, keys=keys) for replay in replays.values()]
    for df_action, df_id in tqdm(zip(dfs_action, replays.keys()), desc="Parsing Replay Errors", total=len(dfs_action),
                                 disable=not verbose):
        for column in range(keys):
            # Retrieve offsets where map should be hit
            ar_map_hit = np.concatenate([
                (hits := osu.hits.offset.loc[osu.hits.column == column].to_numpy()),
                (holds := osu.holds.offset.loc[osu.holds.column == column].to_numpy()),
            ])
            # Retrieve offsets where map should be released
            ar_map_rel = osu.holds.tail_offset.loc[osu.holds.column == column].to_numpy()

            n_hits = len(hits)
            n_holds = len(holds)

            # Retrieve offsets where replays are hit
            ar_rep_hit = df_action.loc[df_action.is_press & (df_action.column == column)].offset.to_numpy()
            ar_map_hit_error = get_error(ar_map_hit, ar_rep_hit)

            # Retrieve offsets where replays are released
            ar_rep_rel = df_action.loc[~df_action.is_press & (df_action.column == column)].offset.to_numpy()
            ar_map_rel_error = get_error(ar_map_rel, ar_rep_rel)

            dfs_error.append(pd.DataFrame(
                data={
                    'replay_id': df_id,
                    'offset': np.concatenate([ar_map_hit, ar_map_rel]).astype(int),
                    'column': column,
                    'category': pd.Series([*("Hit",) * n_hits, *("Hold Head",) * n_holds, *("Hold Tail",) * n_holds],
                                          dtype='category'),
                    'error': np.concatenate([ar_map_hit_error, ar_map_rel_error]).astype(int),
                },
            ).set_index('replay_id', append=True))

    return pd.concat(dfs_error).reorder_levels([1, 0])
