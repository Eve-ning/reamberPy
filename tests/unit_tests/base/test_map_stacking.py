from reamber.base.lists.notes import HitList, HoldList


def test_stack_include(map, offsets, randintp):
    s = map.stack((HitList,))
    s.offset += randintp
    assert all(offsets + randintp == map[HitList][0].offset)
    assert all(offsets == map[HoldList][0].offset)


def test_stack_loc_conditional(map, columns, offsets, randintp):
    s = map.stack()
    s.loc[s.offset < offsets[2], 'column'] += randintp
    assert all(columns[:2] + randintp == map[HitList][0].column[:2])
    assert all(columns[:2] + randintp == map[HoldList][0].column[:2])


def test_stack_loc_conditional_multiple(map, columns, offsets, randintp):
    """ Checks if loc with multiple conditions work """
    s = map.stack()
    s.loc[
        (s.offset > offsets[1]) & (s.column < columns[3]),
        ['offset', 'length']
    ] += randintp
    assert offsets[0] == map[HitList][0].offset[0]
    assert offsets[2] + randintp == map[HitList][0].offset[2]
