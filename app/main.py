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
render_widget(m, m.title + "1s")

# %%
import numpy as np
import pandas as pd


@st.cache_resource
def get_df_jack_bpm(_m: Map, meta):
    meta
    a = Pattern.from_note_lists([_m.hits, _m.holds], include_tails=False).group()
    c = PtnCombo(a).combinations(
        2,
        combo_filter=PtnFilterCombo.create(
            [[0, 0]], 4,
            options=PtnFilterCombo.Option.REPEAT,
            exclude=False
        ).filter,
    )
    return pd.DataFrame(
        [(i['offset'][0, 0],
          np.diff(i['offset'])[0]) for i in c],
        columns=['offset', 'jack_bpm']
    ).explode('jack_bpm').assign(
        jack_bpm=lambda x: 60000 / (x['jack_bpm'].astype(float)) / 4
    )


import altair as alt

df_jack = get_df_jack_bpm(m, meta)
st.dataframe(df_jack)
df_jack['offset_time'] = pd.to_datetime(df_jack['offset'], unit='ms')
df_jack = df_jack.set_index('offset_time')
# %%

df = (
    df_jack
    .groupby(df_jack.jack_bpm // 10)
    .resample('10s')
    .count()
    .drop('jack_bpm', axis=1)
    .reset_index()
    .assign(jack_bpm = lambda x: x.jack_bpm * 10)
    .pivot(columns='jack_bpm', index='offset_time', values='offset')
    .fillna(0)
    .reset_index()
    .assign(
        offset_time=lambda x: x.offset_time.dt.strftime('%M:%S.%f').str[:-3]
    )
    .melt(id_vars='offset_time')
    # .set_index('offset_time')
)

# Set 0 to na
df = df.replace(0, np.nan)
# %%
left, right = st.columns([6, 1])
with right:
    offset_bins = st.slider('Offset Bins', 10, 100, 50)
    jack_bpm_bins = st.slider('Jack Diff Bins', 5, 25, 10)
with left:
    chart = alt.Chart(df).mark_rect().encode(
        alt.X(
            'offset_time:O', title="Offset (ms)",
        ),
        # invert y axis
        alt.Y('jack_bpm:O', title="Jack Distance (ms)", sort='descending'),
        alt.Color('value:Q').scale(scheme='greenblue')
    )
    st.altair_chart(chart, use_container_width=True)
    # %
    # for i in c:
    #     print(i['offset'])
# %%
