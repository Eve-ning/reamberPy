def test_meta(bms_map):
    assert bms_map.title == b'searoad tracks =side blue= (LN-Applied)'
    assert bms_map.artist == b'sasakure.UK / obj:moya'
    assert bms_map.version == b'16'
    assert bms_map.misc[b'GENRE'] == b"Intelligence(7-OriginalEdit)"
