"""Tests for simple tools for timing functions' execution. """

import sys

if sys.version_info[:2] <= (2, 5):
    disabled = True

from sympy.utilities.timeutils import timed

def test_timed():
    result = timed(lambda: 1 + 1, limit=100000)
    assert result[0] == 100000 and result[3] == "ns"

    result = timed("1 + 1", limit=100000)
    assert result[0] == 100000 and result[3] == "ns"