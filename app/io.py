from pathlib import Path

import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from reamber.bms import BMSMap
from reamber.bms.BMSChannel import BMSChannel
from reamber.o2jam import O2JMapSet
from reamber.osu import OsuMap
from reamber.quaver import QuaMap
from reamber.sm import SMMapSet


def read_widget():
    f: UploadedFile = st.file_uploader("Upload a .osu file")
    if f is None:
        f = open(Path(__file__).parents[1] / "rsc/maps/osu/rebirth.osu", "rb")
    file_ext = f.name.split(".")[-1]

    if file_ext == "osu":
        read_fn = lambda x: OsuMap.read(x)
    elif file_ext == "qua":
        read_fn = lambda x: QuaMap.read(x)
    elif file_ext == "sm":
        read_fn = lambda x: SMMapSet.read(x)
    elif file_ext in ("bme", "bms", "bml"):
        read_fn = lambda x: BMSMap.read(
            x, note_channel_config=BMSChannel.BME
        )
    elif file_ext == "pms":
        read_fn = lambda x: BMSMap.read(
            x, note_channel_config=BMSChannel.PMS
        )
    elif file_ext == "ojn":
        read_fn = lambda x: O2JMapSet.read(x)
    else:
        return None

    m = read_fn([fl.decode("utf-8", errors="ignore") for fl in f.readlines()])
    return m, m.metadata()
