import pytest


def test_lengths(hold_list, hold_lengths):
    assert all(hold_lengths == hold_list.length.to_list())


def test_lengths_change(hold_list, hold_lengths, randintp):
    hold_list.length *= randintp
    assert all(hold_lengths * randintp == hold_list.length.to_list())
    assert all(hold_list.offset + hold_lengths * randintp == \
               hold_list.tail_offset.to_list())


@pytest.mark.parametrize(
    'slc,include_head,include_tail',
    [
        (slice(0, 0), False, False),
        (slice(0, 1), False, True),
        (slice(1, 2), True, False),
        (slice(0, 2), True, True),
    ]
)
def test_between(hold_list, offsets, hold_lengths, slc, include_head,
                 include_tail):
    # Hold Lengths are all 50, offsets gaps are 100
    assert (
        (hold_list[slc].to_numpy() ==
         hold_list.between(
             offsets[0] + hold_lengths[0],
             offsets[1],
             include_ends=(True, True),
             include_head=include_head,
             include_tail=include_tail
         ).to_numpy()).all()
    )
