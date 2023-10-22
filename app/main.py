import streamlit as st

from app.density import density_widget
from app.io import read_uploaded_file
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import (
    PFDrawBpm,
    PFDrawBeatLines,
    PFDrawColumnLines,
    PFDrawNotes,
    PFDrawOffsets,
)

st.set_page_config(layout="wide")
st.title("ReamberPy")

with st.sidebar:
    st.header("Data")
    m = read_uploaded_file()
    st.title(m.title)
    # st.dataframe(m.hits.df)

density_widget(m)

# %%
im = (
    PlayField(m=m, duration_per_px=5, padding=40)
    + PFDrawBpm()
    + PFDrawBeatLines()
    + PFDrawColumnLines()
    + PFDrawNotes()
    + PFDrawOffsets()
).export_fold(max_height=5000)

st.image(im, output_format="PNG", width=im.width)
