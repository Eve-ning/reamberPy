import streamlit as st

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import (
    PFDrawBpm,
    PFDrawBeatLines,
    PFDrawColumnLines,
    PFDrawNotes,
)


def render_widget(_m, meta):
    @st.cache_resource
    def make_im():
        return (
            PlayField(m=_m, duration_per_px=5, padding=10)
            + PFDrawBpm()
            + PFDrawBeatLines()
            + PFDrawColumnLines()
            + PFDrawNotes()
        ).export_fold(max_height=1000)

    im = make_im()

    st.download_button(
        f":arrow_down: Download Full Resolution",
        im.tobytes(),
        f"{meta}.png",
        "Click to download",
    )
    st.image(
        im,
        output_format="PNG",
        width=im.width,
        use_column_width=True,
        caption=f"Chart for {meta}",
    )
