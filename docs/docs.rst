
.. toctree::
    :maxdepth: 2
    :hidden:

#############
Documentation
#############

BaseRange
#########

``BaseRange`` is an abstract base class that provides the common interface for
all **OpenRange** objects. Like the built-in ``range`` object, BaseRange is a
subclass of :py:class:`Sequence<collections.Sequence>` and supports all of the
common sequence operations. The constructor for ``BaseRange`` uses the same 
arguments and defaults as the built-in ``range``.

Subclasses of ``BaseRange`` need only define how to convert between the type of
objects within the progression and an underlying numeric type. To do so, these
two abstract methods must be implemented:

.. code-block:: python

    @abstractmethod
    def _item_to_num(self, item):
        """Convert the item to a numerical value."""

    @abstractmethod
    def _num_to_item(self, num):
        """Convert the value to an item in the progression."""
        

For example, to implement a range-like object that generates ``datetime.date``
objects, ``_item_to_num`` would convert a ``datetime.date`` item to a numerical
representation like seconds since the epoch. Conversly, ``_num_to_item`` would
converts seconds since the epoch back to a ``datetime.date`` object. 

Once these two methods are implemented, everything else is handled by
``BaseRange``.

In some cases, the ``step`` type may differ from the items within the
progression.  In this case, a subclass should implement the following
conversion methods:

.. code-block:: python

    @abstractmethod
    def _step_to_num(self, step):
        """Convert supplied step item to a numeric value."""

    @abstractmethod
    def _num_to_step(self, num):
        """Convert supplied numeric value to a step item."""

For the ``datetime.date`` example, the ``step`` would be implemented as a
:py:obj:`datetime.timedelta` object. The ``_step_to_num`` method would convert
a ``datetime.timedelta`` object to seconds whereas ``_num_to_step`` would
convert seconds back to a ``datetime.timedelta`` object.

The default implementations of the ``step`` conversion methods assume the
``step`` is of the same type as ``start`` and ``stop``, and therefore fall back
to calling the ``_item_to_num`` and ``_num_to_item`` methods. 

Example
=======

Here's a simple, yet full implementation of a range-like object that iterates
over strings representing binary numbers.

.. literalinclude:: ../examples/binary_str.py
    :language: python
    
You can see how the two required methods, ``_item_to_num`` and ``_num_to_item``
convert between string and integer values. You can also see the default value
for ``start`` is ``0`` and ``step`` is ``1``, just like the built-in range.

.. note::

    You may have noticed that the ``BaseRange`` implementation is not quite
    identical to the built-in ``range``.  Unlike the built-in ``range``,
    ``BaseRange`` implements iteration as inclusive of the ``stop`` value. The
    built-in ``range`` is exclusive of the ``stop`` value because it is
    commonly used to generate integers for zero-based indexing of lists. The
    typical usage of ``BaseRange`` will likely not be to generate integer types
    and so the decision was made to make the iteration inclusive of the
    ``stop`` value.

.. note::
    
    Like python 2's built-in :py:obj:`xrange` and python 3's built-in
    :py:obj:`range` object, ``BaseRange`` does its best to avoid evaluating
    items in the progression until it has to. In cases where this is
    unavoidable, that method's documentation will say so.

Range
#####

**OpenRange** comes with a generic numerical range-like class called ``Range``.
This class inherits ``BaseRange`` and supports any numeric type (``float``,
``int``, ``decimal.Decimal``, etc.) for its ``start``, ``stop``, and ``step``
values.  Iterating over a ``Range`` object yields ``int`` and/or ``float``
items depending on the values within the progression. 

The primary purpose of ``Range`` is for testing ``BaseRange``, but it can also
be used to show some of the additional features that ``BaseRange`` provides
that don't exist in the built-in ``range``. These features are highlighted in
the sections below.

enumeration
===========

An ``enumerate`` method is available for generating tuples of the form
``(count, item)`` for items within the progression. The method is similar to
python's built-in :py:obj:`enumerate` method, including the optional ``start``
argument.

.. code-block:: python

    >>> from openrange.rng import Range
    >>> for i in Range(-1.0, 1, .5).enumerate():
    ...     print str(i),
    ... 
    (0, -1) (1, -0.5) (2, 0.0) (3, 0.5) (4, 1.0)

    >>> for i in Range(-1, 1, .5).enumerate(start=5):
    ...     print str(i),
    ... 
    (5, -1) (6, -0.5) (7, 0.0) (8, 0.5) (9, 1.0)

exclusion
=========

``BaseRange`` subclasses allow iteration over a progression with the ability 
to exclude certain items. This is possible using the ``excluding`` method 
supplied with a list of items to exclude. The items in the iterable should be
of the same type as the object's ``start`` and ``stop`` arguments.

.. code-block:: python

    >>> from openrange.rng import Range
    >>> for i in Range(-1.0, 1, .5).excluding([0, 1, 10]):
    ...     print str(i),
    ... 
    -1 -0.5 0.5

random iteration
================

Another feature of ``BaseRange`` subclasses is the ability to iterate over
items in the progression in a random order using the ``random`` method. 

.. code-block:: python

    >>> from openrange.rng import Range
    >>> for i in Range(-1.0, 1, .5).random():
    ...     print str(i),
    ... 
    1.0 0.5 -1.0 -0.5 0.0

repeat iteration
================

For cases where iterating of the progression multiple times is useful, the
``repeat`` method can be used. By default, it will generate the items in the
progression 2 times. The optional ``times`` argument can be used to repeat
the items more than twice.

.. code-block:: python

    >>> from openrange.rng import Range
    >>> for i in Range(-1, 1, .5).repeat():
    ...     print str(i),
    ... 
    -1 -0.5 0.0 0.5 1.0 -1 -0.5 0.0 0.5 1.0

    >>> for i in Range(-1, 1, .5).repeat(times=3):
    ...     print str(i),
    ... 
    -1 -0.5 0.0 0.5 1.0 -1 -0.5 0.0 0.5 1.0 -1 -0.5 0.0 0.5 1.0

``datetime`` Ranges
###################

**OpenRange** comes with 3 additional example range-like implementations based
on types defined in python's :py:obj:`datetime` module. These objects are
highlighted in the following sections.

DateRange
=========

``DateRange`` generates ``datetime.date`` objects between given ``start`` and
``stop`` ``datetime.date`` objects. The ``step`` value is provided as a
``datetime.timedelta`` object. Here are some examples:

.. literalinclude:: ../examples/date_range.py
    :language: python

DatetimeRange
=============

``DatetimeRange`` generates ``datetime.datetime`` objects between given
``start`` and ``stop`` ``datetime.datetime`` objects. The ``step`` value is
provided as a ``datetime.timedelta`` object. Here are some examples: 

.. literalinclude:: ../examples/datetime_range.py
    :language: python

TimeRange
=========

``TimeRange`` generates ``datetime.time`` objects between given ``start`` and
``stop`` ``datetime.time`` objects. The ``step`` value is provided as a
``datetime.timedelta`` object. Here are some examples:

.. literalinclude:: ../examples/time_range.py
    :language: python

