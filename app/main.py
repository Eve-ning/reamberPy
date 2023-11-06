import streamlit as st

from app.density import density_widget
from app.io import read_widget
from app.render import render_widget
from reamber.algorithms.pattern import Pattern
from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.pattern.filters import PtnFilterCombo

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
a = Pattern.from_note_lists([m.hits]).group()
c = PtnCombo(a).combinations(
    2,
    combo_filter=PtnFilterCombo.create(
        [[0, 0]], 4, options=PtnFilterCombo.Option.REPEAT, exclude=False
    ).filter,
)

c
