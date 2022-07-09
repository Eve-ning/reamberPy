import numpy as np

from reamber.algorithms.pattern.filters import PtnFilterType
from reamber.base.Hit import Hit
from reamber.base.Hold import Hold


def test_type():
    assert np.all(
        PtnFilterType.create(
            [[Hit, Hold]]
        ).ar == np.array([Hit, Hold])
    )


def test_type_any_order():
    assert np.all(
        PtnFilterType.create(
            [[Hit, Hit, Hold]],
            options=PtnFilterType.Option.ANY_ORDER
        ).ar == np.array([[Hit, Hit, Hold],
                          [Hit, Hold, Hit],
                          [Hold, Hit, Hit]])
    )


def test_type_mirror():
    assert np.all(
        PtnFilterType.create(
            [[Hit, Hit, Hold]],
            options=PtnFilterType.Option.MIRROR
        ).ar == np.array([[Hit, Hit, Hold], [Hold, Hit, Hit]])
    )


def test_type_any_order_mirror():
    assert np.all(
        PtnFilterType.create(
            [[Hit, Hit, Hold]],
            options=PtnFilterType.Option.ANY_ORDER |
                    PtnFilterType.Option.MIRROR
        ).ar == np.array([[Hit, Hit, Hold],
                          [Hit, Hold, Hit],
                          [Hold, Hit, Hit]])
    )

