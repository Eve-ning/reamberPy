def test_length(holds, hold_lengths):
    assert hold_lengths[0] == holds[0].length


def test_tail_offset(holds, offsets, hold_lengths):
    assert offsets[0] + hold_lengths[0] == holds[0].tail_offset


def test_length_op(holds, offsets, hold_lengths, randintp):
    holds[0].length *= randintp
    assert hold_lengths[0] * randintp == holds[0].length
    assert offsets[0] + hold_lengths[0] * randintp == holds[0].tail_offset
    # An odd occurrence, but we support negative lengths.
    holds[0].length = -randintp
    assert -randintp == holds[0].length
    assert offsets[0] - randintp == holds[0].tail_offset
