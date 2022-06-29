from reamber.quaver import QuaSv


def test_from_yaml_dict():
    sv = QuaSv.from_yaml(dict(StartTime=1000, Multiplier=2.0))
    assert sv == QuaSv(offset=1000, multiplier=2.0)
    return sv


def test_to_yaml_dict():
    assert test_from_yaml_dict().to_yaml() == dict(StartTime=1000,
                                                   Multiplier=2.0)
