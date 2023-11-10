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
render_widget(m, meta)

# %%
import numpy as np
import pandas as pd


@st.cache_resource
def get_df_jack_diff(_m: Map, meta):
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
        columns=['offset', 'jack_diff']
    ).explode('jack_diff').assign(
        jack_diff=lambda x: np.log(x['jack_diff'].astype(float))
    )


import altair as alt

df_jack_diff = get_df_jack_diff(m, meta)

left, right = st.columns([6, 1])
with right:
    offset_bins = st.slider('Offset Bins', 10, 100, 50)
    jack_diff_bins = st.slider('Jack Diff Bins', 5, 25, 10)
with left:
    chart = alt.Chart(df_jack_diff).mark_rect().encode(
        alt.X('offset:Q',title="Offset (ms)").bin(offset_bins),
        alt.Y('jack_diff:Q', title="Log Jack Difference").bin(maxbins=jack_diff_bins),
        alt.Color('count():Q').scale(scheme='greenblue')
    ).mark_rect().encode()
    st.altair_chart(chart, use_container_width=True)
    # %
    # for i in c:
    #     print(i['offset'])
#     break
# c[2]['offset']
