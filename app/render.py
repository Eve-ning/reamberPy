import io

import streamlit as st

from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import (
    PFDrawBpm,
    PFDrawBeatLines,
    PFDrawColumnLines,
    PFDrawNotes,
PFDrawOffsets
)


def render_widget(_m, meta):
    @st.cache_resource
    def make_im(meta):
        return (
            PlayField(m=_m, duration_per_px=10, padding=60)
            + PFDrawBpm()
            + PFDrawBeatLines()
            + PFDrawColumnLines()
            + PFDrawNotes()
            + PFDrawOffsets(interval=1000)
        ).export_fold(max_height=1000)

    im = make_im(meta)

    im_b = io.BytesIO()
    # image.save expects a file-like as a argument
    im.save(im_b, format="PNG")
    st.download_button(
        f":arrow_down: Download Full Resolution",
        im_b.getvalue(),
        fr"im.png",
        "Click to download",
    )
    st.image(
        im,
        output_format="PNG",
        width=im.width,
        use_column_width=True,
        caption=f"Chart for {meta}",
    )
