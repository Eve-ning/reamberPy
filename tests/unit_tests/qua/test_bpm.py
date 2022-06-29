from reamber.quaver import QuaBpm


def test_from_yaml_dict():
    bpm = QuaBpm.from_yaml(dict(StartTime=1000, Bpm=100))
    assert bpm == QuaBpm(offset=1000, bpm=100, metronome=4)
    return bpm


def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml() == dict(StartTime=1000, Bpm=100)
