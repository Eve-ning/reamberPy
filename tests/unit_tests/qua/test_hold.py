from reamber.quaver import QuaHold


def test_from_yaml_dict():
    obj = QuaHold.from_yaml(
        dict(StartTime=1000, Lane=1, KeySounds=['a.wav', 'b.wav'],
             EndTime=2000))
    assert obj == QuaHold(offset=1000, column=0, keysounds=['a.wav', 'b.wav'],
                          length=1000)
    return obj


def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml() == \
           dict(StartTime=1000, Lane=1, KeySounds=['a.wav', 'b.wav'],
                EndTime=2000)
