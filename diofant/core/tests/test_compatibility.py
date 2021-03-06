import pytest

from diofant.core.compatibility import (default_sort_key, as_int, ordered,
                                        iterable)
from diofant.core.singleton import S

from diofant.abc import x

__all__ = ()


def test_default_sort_key():
    def func(x):
        return x
    assert sorted([func, x, func], key=default_sort_key) == [func, func, x]


def test_as_int():
    pytest.raises(ValueError, lambda: as_int(1.1))
    pytest.raises(ValueError, lambda: as_int([]))
    pytest.raises(ValueError, lambda: as_int(S.NaN))
    pytest.raises(ValueError, lambda: as_int(S.Infinity))
    pytest.raises(ValueError, lambda: as_int(S.NegativeInfinity))
    pytest.raises(ValueError, lambda: as_int(S.ComplexInfinity))


def test_iterable():
    assert iterable(0) is False
    assert iterable(1) is False
    assert iterable(None) is False


def test_ordered():
    # Issue sympy/sympy#7210 - this had been failing with python2/3 problems
    assert (list(ordered([{1: 3, 2: 4, 9: 10}, {1: 3}])) ==
            [{1: 3}, {1: 3, 2: 4, 9: 10}])
    # warnings should not be raised for identical items
    l = [1, 1]
    assert list(ordered(l, warn=True)) == l
    l = [[1], [2], [1]]
    assert list(ordered(l, warn=True)) == [[1], [1], [2]]
    pytest.raises(ValueError, lambda: list(ordered(['a', 'ab'],
                                                   keys=[lambda x: x[0]],
                                                   default=False,
                                                   warn=True)))
    pytest.raises(ValueError, lambda: list(ordered(['a', 'b'], default=False)))
