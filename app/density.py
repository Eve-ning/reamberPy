import altair as alt
import pandas as pd
import streamlit as st

from reamber.base import Map


def get_density_s(
    sr: pd.Series,
    name: str = "density",
    groupby_ms: int = 3000,
) -> pd.Series:
    sr = sr.groupby(sr // groupby_ms).count().rename(name) * 1000 / groupby_ms
    sr.index.name = "offset"
    sr.index *= groupby_ms
    return sr


def plot_density(
    srs: dict[str, pd.Series],
    precision: int = 2,
    groupby_ms: int = 3000,
):
    # TODO: Pretty annoying to deal with ms data, altair doesn't like datetime
    #  so we have to convert to str. If we can make it work with datetime, we
    #  can make the ticks more readable as 00:00, 01:00, 02:00 etc.
    df = (
        pd.concat(
            [get_density_s(sr, name, groupby_ms) for name, sr in srs.items()],
            axis=1,
            join="outer",
        )
        .reset_index()
        .melt(id_vars="offset", var_name="note_type", value_name="density")
        .astype({"offset": "datetime64[ms]"})
        .assign(offset=lambda df: df["offset"].dt.time.astype(str))
    )

    st.altair_chart(
        alt.Chart(df.round(precision), title="Density Plot")
        .mark_rect()
        .encode(
            x=alt.X("offset:O").axis(title="Offset", labelAngle=0),
            y=alt.X("density").axis(title="Density/s"),
            opacity=alt.value(0.8),
            color=alt.Color("note_type", title="Note Type"),
            tooltip=alt.Tooltip(
                ["offset", "density", "note_type"],
            ),
        ),
        use_container_width=True,
    )


def density_widget(
    m: Map,
):
    left, right = st.columns([6, 1])
    with right:
        hits = st.checkbox("Hits", value=True)
        hold_heads = st.checkbox("Holds", value=True)
        groupby_ms = st.slider("Group By (ms)", 1000, 15000, 3000, 1000)
    with left:
        d = {}
        if hits:
            d["Hits"] = m.hits.offset
        if hold_heads:
            d["Hold Heads"] = m.holds.offset
        plot_density(d, groupby_ms=groupby_ms)
