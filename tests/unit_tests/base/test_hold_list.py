import pandas as pd

from reamber.base.lists.notes.HoldList import HoldList


def test_type(hold_list):
    assert isinstance(hold_list.df, pd.DataFrame)


def test_lengths(hold_list):
    assert [500, 500, 1000, 1000] == hold_list.length.to_list()


def test_lengths_change(hold_list):
    hold_list.length *= 10
    [5000, 5000, 10000, 10000] == hold_list.length.to_list()
    [5000, 6000, 12000, 13000] == hold_list.tail_offset.to_list()


def test_offsets(hold_list):
    assert [0, 1000, 2000, 3000] == hold_list.offset.to_list()
    assert [0, 1000, 2000, 3000] == hold_list.head_offset.to_list()
    assert [500, 1500, 3000, 4000] == hold_list.tail_offset.to_list()


def test_init_single_and_multiple(holds):
    """ Tests whether initializing with a single item list is different from a single item """
    assert HoldList(holds[0:1]) == HoldList(holds[0])


def test_ix_slice(hold_list, holds):
    a = hold_list[0:2]
    assert isinstance(a, HoldList)
    assert 2 == len(a)
    assert HoldList(holds[0:2]) == a


def test_ix_bool(hold_list):
    a = hold_list[hold_list.length < 1000]
    assert isinstance(a, HoldList)
    assert 2 == len(a)
    assert 500 == a[0].length
    assert 500 == a[1].length
    assert 0 == a[0].offset
    assert 1000 == a[1].offset


def test_in_columns(hold_list):
    a = hold_list.in_columns([2, 3])
    assert (2, len(a))
    assert (1000, a[0].offset)
    assert (2000, a[1].offset)

    # Assert that this is a deepcopy.
    a.iloc[0].offset += 500
    assert (1000, hold_list[1].offset)
    assert (1500, a[0].offset)


def test_first_last_offset(hold_list):
    assert (0, hold_list.first_offset())
    assert (4000, hold_list.last_offset())
    assert ((0, 4000), hold_list.first_last_offset())


def test_empty_handling(hold_list):
    # Check if empty initialization works
    assert HoldList([]).column == hold_list.between(500, 750).column
    # Check if truly empty
    assert HoldList([]).df.empty
    assert hold_list.between(500, 750).df.empty


def test_describe(hold_list):
    assert isinstance(hold_list.df.describe(), pd.DataFrame)


def test_rolling(hold_list):
    assert {0: 1, 1000: 1, 2000: 1, 3000: 1} == hold_list.rolling_density(1000)
    assert {0: 1, 500: 1, 1000: 1, 1500: 1, 2000: 1, 2500: 1, 3000: 1,
            3500: 0} == hold_list.rolling_density(1000, 500)
    assert {0: 1, 500: 0, 1000: 1, 1500: 0, 2000: 1, 2500: 0, 3000: 1,
            3500: 0} == hold_list.rolling_density(500)

    def test_activity(hold_list):
        # noinspection PyTypeChecker
        assert [1000, 1000, 1000, 1000] == hold_list.activity().tolist()

    def test_between(hold_list, holds):
        """
            0         1000
            [----]    [----]
               500      1500
        """
        # [---------)
        # [----]    [----]
        assert (
            (HoldList(holds[0]).to_numpy() ==
             hold_list.between(0, 1000, include_ends=(True, False),
                               include_head=True, include_tail=False)
             .to_numpy()).all())

        #  [--------)
        # [----]    [----]
        assert (
            (HoldList([]).to_numpy() ==
             hold_list.between(100, 1000, include_ends=(True, False),
                               include_head=True, include_tail=False)
             .to_numpy()).all())

        #      [----)
        # [----]    [----]
        assert (
            (HoldList(holds[0]).to_numpy() ==
             hold_list.between(500, 1000, include_ends=(True, False),
                               include_head=True, include_tail=True)
             .to_numpy()).all())

        #      (----)
        # [----]    [----]
        assert (
            (HoldList([]).to_numpy() ==
             hold_list.between(500, 1000, include_ends=(False, False),
                               include_head=True, include_tail=True)
             .to_numpy()).all())

        #      [----]
        # [----]    [----]
        assert (
            (HoldList(holds[0:2]).to_numpy() ==
             hold_list.between(500, 1000, include_ends=(True, True),
                               include_head=True, include_tail=True)
             .to_numpy()).all())

        #      [-----]
        # [----]    [----]
        assert (
            (HoldList(holds[0]).to_numpy() ==
             hold_list.between(500, 1100, include_ends=(True, True),
                               include_head=False, include_tail=True)
             .to_numpy()).all())
