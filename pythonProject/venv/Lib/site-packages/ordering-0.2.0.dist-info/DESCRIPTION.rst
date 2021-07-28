Python Order Maintenance
========================

A data structure to `impose a total order <https://en.wikipedia.org/wiki/Order-maintenance_problem>`_ on a collection of objects.

Dependencies
------------

``ordering`` requires Python 3.6+.
If the type hints were removed, it would probably work in earlier versions, as well.

Usage
-----

An ordering is represented by an Ordering object.
The order may be different to the usual order between objects, or even between objects that are not normally comparable.

.. code:: python

    >>> from ordering import Ordering
    >>> order = Ordering([2, 0, 1])

We can then compare the objects in our ordering, to check if the first object comes before the second in the order.

.. code:: python

    >>> order.compare(0, 1) # 1 after 0
    True
    >>> order.compare(0, 2) # 2 before 0
    False

Our ordering is mutable, and we can add elements on either end, or immediately before or after an existing element.

.. code:: python

    >>> order.insert_end(3) # Add 3 on the end
    >>> order.compare(1, 3) # 3 after 1
    True

    >>> order.insert_after(0, 4) # Insert 4 immediately after 0
    >>> order.compare(0, 4) # 4 after 0
    True
    >>> order.compare(1, 4) # 4 before 1
    False

Orderings are iterable, yielding their items in order.

.. code:: python

    >>> list(order)
    [2, 0, 4, 1, 3]

And can be used as a key in sorting functions, to sort with respect to that order.

.. code:: python

    >>> sorted(range(3), key=order)
    [2, 0, 1]


