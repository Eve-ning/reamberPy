def test_in_columns(hit_list, offsets, columns):
    in_cols = hit_list.in_columns(columns[:2])
    assert 2 == len(in_cols)
    assert all(hit_list[:2] == in_cols)
