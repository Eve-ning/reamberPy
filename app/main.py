import streamlit as st

from app.density import density_widget
from app.io import read_widget
from app.render import render_widget
from reamber.algorithms.pattern import Pattern
from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.pattern.filters import PtnFilterCombo
from reamber.base import Map

st.set_page_config(layout="wide")
st.title("ReamberPy")

with st.sidebar:
    st.header("Data")
    m, meta = read_widget()
    st.title(m.title)

st.subheader("Density")
density_widget(m)

st.subheader("Render")
render_widget(m, m.title)

# %%
import numpy as np
import pandas as pd


# @st.cache_resource
def get_df_jack_bpm(_m: Map, meta):

    ptn = Pattern.from_note_lists([_m.hits, _m.holds],
                                  include_tails=False).group()
    combos = PtnCombo(ptn).combinations(
        2,
        combo_filter=PtnFilterCombo.create(
            [[0, 0]], _m.stack().column.max(),
            options=PtnFilterCombo.Option.REPEAT,
            exclude=False
        ).filter,
    )
    # st.write(combos)
    df = pd.DataFrame(
        [(i['offset'][0, 0],
          np.diff(i['offset'])[0]) for i in combos],
        columns=['offset', 'jack_bpm']
    ).explode('jack_bpm').assign(
        jack_bpm=lambda x: 60000 / (x['jack_bpm'].astype(float)) / 4,
        offset=lambda x: pd.to_datetime(x['offset'], unit='ms')
    ).set_index('offset')
    return df


def pivot_jack(df: pd.DataFrame, bpm_bin: int = 10, offset_bin: str = '1s'):
    return (
        df.iloc[:, 0]
        .groupby(df_jack.jack_bpm // bpm_bin * bpm_bin)
        .resample(offset_bin)
        .count()
        .rename('n')
        .reset_index()
        .pivot(columns='jack_bpm', index='offset', values='n')
    )


def fill_missing(df: pd.DataFrame, bpm_bin: int = 10):
    return (
        # Fill missing bpm bins
        df.join(
            pd.DataFrame(columns=list(
                filter(lambda x: x not in df.columns,
                       np.arange(df.columns.min(),
                                 df.columns.max(),
                                 bpm_bin))),
            ),
            how='outer',
        )
        # Sort by columns
        .sort_index(axis=1)
        .reset_index()
        .assign(
            offset=lambda x: x.offset.dt.strftime('%M:%S.%f').str[:-3]
        )
        .melt(id_vars='offset', var_name='jack_bpm', value_name='n')
        .replace(0, np.nan)#.dropna()
    )


import altair as alt

left, right = st.columns([6, 1])
with right:
    offset_bin = st.select_slider(
        'Offset Bins',
        ['250ms', '500ms', '1s', '2s', '5s', '10s', '20s', '30s', '1min'],
        value='2s'
    )
    jack_bpm_bin = st.slider('Jack Diff Bins', 5, 50, 10, 5)

    df_jack = get_df_jack_bpm(m, meta)
    df = pivot_jack(df_jack, bpm_bin=jack_bpm_bin, offset_bin=offset_bin)
    df = fill_missing(df, bpm_bin=jack_bpm_bin)
with left:
    chart = alt.Chart(df).mark_point(strokeWidth=4, size=180).encode(
        alt.X('offset:O', title="Offset (ms)"),
        alt.Y('jack_bpm:O', title="Jack BPM (1/4s)",
              sort='descending'),
        alt.Color('n:Q')
        .scale(scheme='plasma')
    )
    st.altair_chart(chart, use_container_width=True)
