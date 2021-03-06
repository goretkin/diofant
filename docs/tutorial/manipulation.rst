==================
 Expression Trees
==================

..
   >>> from diofant import *
   >>> x, y, z = symbols('x y z')
   >>> init_printing(pretty_print=True, use_unicode=True)

In this section, we discuss some ways that we can perform advanced
manipulation of expressions.

Before we can do this, we need to understand how expressions are
represented in Diofant.  A mathematical expression is represented as a
tree.  Let us take the expression `x y + x^2`.  We can see what this
expression looks like internally by using :func:`repr`

    >>> repr(x*y + x**2)
    "Add(Pow(Symbol('x'), Integer(2)), Mul(Symbol('x'), Symbol('y')))"

The easiest way to tear this apart is to look at a diagram of the
expression tree:

.. This comes from dotprint(x**2 + x*y, labelfunc=repr)

.. graphviz::

    digraph{

    # Graph style
    "bgcolor"="transparent"
    "ordering"="out"
    "rankdir"="TD"

    #########
    # Nodes #
    #########

    "Add(Pow(Symbol('x'), Integer(2)), Mul(Symbol('x'), Symbol('y')))_()" ["color"="black", "label"="Add", "shape"="ellipse"];
    "Pow(Symbol('x'), Integer(2))_(0,)" ["color"="black", "label"="Pow", "shape"="ellipse"];
    "Symbol('x')_(0, 0)" ["color"="black", "label"="Symbol('x')", "shape"="ellipse"];
    "Integer(2)_(0, 1)" ["color"="black", "label"="Integer(2)", "shape"="ellipse"];
    "Mul(Symbol('x'), Symbol('y'))_(1,)" ["color"="black", "label"="Mul", "shape"="ellipse"];
    "Symbol('x')_(1, 0)" ["color"="black", "label"="Symbol('x')", "shape"="ellipse"];
    "Symbol('y')_(1, 1)" ["color"="black", "label"="Symbol('y')", "shape"="ellipse"];

    #########
    # Edges #
    #########

    "Add(Pow(Symbol('x'), Integer(2)), Mul(Symbol('x'), Symbol('y')))_()" -> "Pow(Symbol('x'), Integer(2))_(0,)";
    "Add(Pow(Symbol('x'), Integer(2)), Mul(Symbol('x'), Symbol('y')))_()" -> "Mul(Symbol('x'), Symbol('y'))_(1,)";
    "Pow(Symbol('x'), Integer(2))_(0,)" -> "Symbol('x')_(0, 0)";
    "Pow(Symbol('x'), Integer(2))_(0,)" -> "Integer(2)_(0, 1)";
    "Mul(Symbol('x'), Symbol('y'))_(1,)" -> "Symbol('x')_(1, 0)";
    "Mul(Symbol('x'), Symbol('y'))_(1,)" -> "Symbol('y')_(1, 1)";
    }

First, let's look at the leaves of this tree.  We got here instances
of the :class:`~diofant.core.symbol.Symbol` class and the Diofant
version of integers, instance of the
:class:`~diofant.core.numbers.Integer` class, even technically we
input integer literal ``2``.

What about ``x*y``?  As we might expect, this is the multiplication of
``x`` and ``y``.  The Diofant class for multiplication is
:class:`~diofant.core.mul.Mul`.

    >>> repr(x*y)
    "Mul(Symbol('x'), Symbol('y'))"

Thus, we could have created the same object by writing

    >>> Mul(x, y)
    x⋅y

When we write ``x**2``, this creates a
:class:`~diofant.core.power.Pow` class instance.

    >>> repr(x**2)
    "Pow(Symbol('x'), Integer(2))"

We could have created the same object by calling

    >>> Pow(x, 2)
     2
    x

Now we get to our final expression, ``x*y + x**2``.  This is the
addition of our last two objects.  The Diofant class for addition is
:class:`~diofant.core.add.Add`, so, as you might expect, to create
this object, we could use

    >>> Add(Pow(x, 2), Mul(x, y))
     2
    x  + x⋅y
    >>> x*y + x**2
     2
    x  + x⋅y

.. note::

   You may have noticed that the order we entered our expression and
   the order that it came out from printers like :func:`repr` or in
   the graph were different.  This because in Diofant, the arguments
   of :class:`~diofant.core.add.Add` and the commutative arguments of
   :class:`~diofant.core.mul.Mul` are stored in an arbitrary (but
   consistent!) order, which is independent of the order inputted.

There is no subtraction class in Diofant.  ``x - y`` is represented as
``x + (-1)*y``

    >>> repr(x - y)
    "Add(Symbol('x'), Mul(Integer(-1), Symbol('y')))"

.. dotprint(x - y, labelfunc=repr)

.. graphviz::

    digraph{

    # Graph style
    "bgcolor"="transparent"
    "ordering"="out"
    "rankdir"="TD"

    #########
    # Nodes #
    #########

    "Add(Symbol('x'), Mul(Integer(-1), Symbol('y')))_()" ["color"="black", "label"="Add", "shape"="ellipse"];
    "Symbol('x')_(0,)" ["color"="black", "label"="Symbol('x')", "shape"="ellipse"];
    "Mul(Integer(-1), Symbol('y'))_(1,)" ["color"="black", "label"="Mul", "shape"="ellipse"];
    "Integer(-1)_(1, 0)" ["color"="black", "label"="Integer(-1)", "shape"="ellipse"];
    "Symbol('y')_(1, 1)" ["color"="black", "label"="Symbol('y')", "shape"="ellipse"];

    #########
    # Edges #
    #########

    "Add(Symbol('x'), Mul(Integer(-1), Symbol('y')))_()" -> "Symbol('x')_(0,)";
    "Add(Symbol('x'), Mul(Integer(-1), Symbol('y')))_()" -> "Mul(Integer(-1), Symbol('y'))_(1,)";
    "Mul(Integer(-1), Symbol('y'))_(1,)" -> "Integer(-1)_(1, 0)";
    "Mul(Integer(-1), Symbol('y'))_(1,)" -> "Symbol('y')_(1, 1)";
    }

Similarly to subtraction, there is no division class.

    >>> repr(x/y)
    "Mul(Symbol('x'), Pow(Symbol('y'), Integer(-1)))"

.. dotprint(x/y, labelfunc=repr)

.. graphviz::

    digraph{

    # Graph style
    "bgcolor"="transparent"
    "ordering"="out"
    "rankdir"="TD"

    #########
    # Nodes #
    #########

    "Mul(Symbol('x'), Pow(Symbol('y'), Integer(-1)))_()" ["color"="black", "label"="Mul", "shape"="ellipse"];
    "Symbol('x')_(0,)" ["color"="black", "label"="Symbol('x')", "shape"="ellipse"];
    "Pow(Symbol('y'), Integer(-1))_(1,)" ["color"="black", "label"="Pow", "shape"="ellipse"];
    "Symbol('y')_(1, 0)" ["color"="black", "label"="Symbol('y')", "shape"="ellipse"];
    "Integer(-1)_(1, 1)" ["color"="black", "label"="Integer(-1)", "shape"="ellipse"];

    #########
    # Edges #
    #########

    "Mul(Symbol('x'), Pow(Symbol('y'), Integer(-1)))_()" -> "Symbol('x')_(0,)";
    "Mul(Symbol('x'), Pow(Symbol('y'), Integer(-1)))_()" -> "Pow(Symbol('y'), Integer(-1))_(1,)";
    "Pow(Symbol('y'), Integer(-1))_(1,)" -> "Symbol('y')_(1, 0)";
    "Pow(Symbol('y'), Integer(-1))_(1,)" -> "Integer(-1)_(1, 1)";
    }

We see that ``x/y`` is represented as ``x*y**(-1)``.

But what about ``x/2``?  Following the pattern of the previous
example, we might expect to see ``Mul(x, Pow(Integer(2), -1))``.  But
instead, we have

    >>> repr(x/2)
    "Mul(Rational(1, 2), Symbol('x'))"

Rational numbers are always combined into a single term in a
multiplication, so that when we divide by 2, it is represented as
multiplying by 1/2.

Walking the Tree
================

Let's look at how to dig our way through an expression tree.  For this
every object in Diofant has a very generic interface --- two important
attributes, :attr:`~diofant.core.basic.Basic.func`, and
:attr:`~diofant.core.basic.Basic.args`.

The head of the object is encoded in the
:attr:`~diofant.core.basic.Basic.func` attribute.  Usually it is the
same as the class of the object, but not always.

    >>> expr = 2 + x*y
    >>> expr
    x⋅y + 2
    >>> expr.func
    <class 'diofant.core.add.Add'>
    >>> type(expr)
    <class 'diofant.core.add.Add'>

The class of an object need not be the same as the one used to create
it.

    >>> Add(x, x)
    2⋅x
    >>> _.func
    <class 'diofant.core.mul.Mul'>

.. note::

   Diofant classes make heavy use of the :meth:`~object.__new__` class
   constructor, which, unlike :meth:`~object.__init__`, allows a
   different class to be returned from the constructor.

The children of a node in the tree are held in the
:attr:`~diofant.core.basic.Basic.args` attribute.

    >>> expr.args
    (2, x⋅y)

From this, we can see ``expr`` can be completely reconstructed from
its :attr:`~diofant.core.basic.Basic.func` and its
:attr:`~diofant.core.basic.Basic.args`.

    >>> expr.func(*expr.args)
    x⋅y + 2

.. note::

   Every well-formed Diofant expression must either have empty
   :attr:`~diofant.core.basic.Basic.args` or satisfy invariant

       >>> expr == expr.func(*expr.args)
       True

In Diofant, empty :attr:`~diofant.core.basic.Basic.args` signal that
we have hit a leaf of the expression tree.

    >>> x.args
    ()
    >>> Integer(2).args
    ()

This interface allows us to write simple algorithms that walk
expression trees.

    >>> def pre(expr):
    ...     yield expr
    ...     for arg in expr.args:
    ...         for subtree in pre(arg):
    ...             yield subtree

See how nice it is that empty :class:`tuple` signals leaves in the
expression tree.  We don't even have to write a base case for our
recursion --- it is handled automatically by the for loop.

Let's test this by printing all nodes of the expression at each level.

    >>> expr = x*y + 2
    >>> for term in pre(expr):
    ...     print(term)
    x*y + 2
    2
    x*y
    x
    y

Can you guess why we called our function ``pre``?  We just wrote a
pre-order traversal function for our expression tree.  See if you can
write a post-order traversal function.

Such traversals are so common in Diofant that the generator functions
:func:`~diofant.core.basic.preorder_traversal` and
:func:`~diofant.utilities.iterables.postorder_traversal` are provided
to make such traversals easy.  We could have also written our test as

    >>> for arg in preorder_traversal(expr):
    ...     print(arg)
    x*y + 2
    2
    x*y
    x
    y
