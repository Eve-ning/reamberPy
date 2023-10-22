import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from reamber.bms import BMSMap
from reamber.bms.BMSChannel import BMSChannel
from reamber.o2jam import O2JMapSet
from reamber.osu import OsuMap
from reamber.quaver import QuaMap
from reamber.sm import SMMapSet


def read_uploaded_file():
    f: UploadedFile = st.file_uploader("Upload a .osu file")

    match f.name.split(".")[-1]:
        case "osu":
            read_fn = lambda x: OsuMap.read(x)
        case "qua":
            read_fn = lambda x: QuaMap.read(x)
        case "sm":
            read_fn = lambda x: SMMapSet.read(x)
        case "bme" | "bms" | "bml":
            read_fn = lambda x: BMSMap.read(
                x, note_channel_config=BMSChannel.BME
            )
        case "pms":
            read_fn = lambda x: BMSMap.read(
                x, note_channel_config=BMSChannel.PMS
            )
        case "ojn":
            read_fn = lambda x: O2JMapSet.read(x)
        case _:
            return None

    return read_fn(
        [fl.decode("utf-8", errors="ignore") for fl in f.readlines()]
    )
