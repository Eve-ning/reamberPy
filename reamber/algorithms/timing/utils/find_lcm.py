from __future__ import annotations

from typing import List

import numpy as np


def find_lcm(a: List, threshold: int) -> list:
    """Find the LCM of each value lower than the threshold

    Examples:
        Take 4 numbers (1, 2, 3, 7), we find their respective LCM lower than n

        n | 15 | 9 | 5 |   n = 9 prevents 15 from forming
        --+----+---+---+
        1 | 15 | 6 | 2 |
        2 | 15 | 6 | 2 |
        3 | 15 | 6 | 3 |
        5 | 15 | 5 | 5 |

    Returns:
        Dict of input (key) and LCM (value)

    Args:
        a: List to reduce
        threshold: Highest value of LCM (exclusive)
    """
    a_ = [0 for _ in a]
    length = len(a)
    for i in range(length):
        for j in range(length):
            if i == j: continue
            b, c = a[i], a[j]
            if b is None or c is None: continue
            lcm = np.lcm(b, c)
            if lcm < threshold:
                a[i] = lcm
                a_[j] = lcm
                a[j] = None

    for i in range(length):
        if a_[i] == 0:
            a_[i] = a[i]

    return a_
