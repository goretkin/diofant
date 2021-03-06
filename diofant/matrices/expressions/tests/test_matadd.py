from diofant.matrices.expressions import MatrixSymbol, MatAdd, MatPow, MatMul
from diofant.matrices import eye, ImmutableMatrix
from diofant import Basic

__all__ = ()

X = MatrixSymbol('X', 2, 2)
Y = MatrixSymbol('Y', 2, 2)


def test_sort_key():
    assert MatAdd(Y, X).doit().args == (X, Y)


def test_matadd_sympify():
    assert isinstance(MatAdd(eye(1), eye(1)).args[0], Basic)


def test_matadd_of_matrices():
    assert MatAdd(eye(2), 4*eye(2), eye(2)).doit() == ImmutableMatrix(6*eye(2))


def test_doit_args():
    A = ImmutableMatrix([[1, 2], [3, 4]])
    B = ImmutableMatrix([[2, 3], [4, 5]])
    assert MatAdd(A, MatPow(B, 2)).doit() == A + B**2
    assert MatAdd(A, MatMul(A, B)).doit() == A + A*B
    assert (MatAdd(A, X, MatMul(A, B), Y, MatAdd(2*A, B)).doit() ==
            MatAdd(X, Y, 3*A + A*B + B))


def test_is_commutative():
    A = MatrixSymbol('A', 2, 2, commutative=True)
    B = MatrixSymbol('B', 2, 2, commutative=True)
    assert (A + B).is_commutative
    assert (A + X).is_commutative is False
