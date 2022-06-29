from reamber.quaver import QuaHit


def test_from_yaml_dict():
    obj = QuaHit.from_yaml(
        dict(StartTime=1000, Lane=1, KeySounds=['a.wav', 'b.wav']))
    assert obj == QuaHit(offset=1000, column=0, keysounds=['a.wav', 'b.wav'])
    return obj


def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml() == dict(StartTime=1000, Lane=1,
                                                   KeySounds=['a.wav',
                                                              'b.wav'])
