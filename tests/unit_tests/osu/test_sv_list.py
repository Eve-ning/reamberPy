from reamber.osu.lists.OsuSvList import OsuSvList


def test_df_names(sv_list):
    assert {'offset', 'multiplier', 'metronome', 'sample_set',
            'sample_set_index', 'volume', 'kiai'} == \
           set(sv_list.df.columns)


def test_read(sv_strings, sv_muls, offsets):
    svs = OsuSvList.read(sv_strings)
    assert (sv_muls == svs.multiplier.to_list()).all()
    assert (offsets == svs.offset.to_list()).all()


def test_write(sv_strings, sv_list):
    assert sv_strings == sv_list.write()
