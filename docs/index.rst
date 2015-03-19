:tocdepth: 2

#########
OpenRange
#########

**OpenRange** provides a simple interface for building custom range-like 
objects for any type that can be represented numerically. 

Overview
########

Python's built-in :py:obj:`range` is great for generating a list of integers
and when iterating over the indices of a sequence. There are times, however,
when you'd like a similar interface for non-integer types. 

The idea behind **OpenRange** is to provide a base class that allows for quick
implementation of arithmetic progressions for any type that can be represented
numerically. For example, you might be interested in a range-like object for
iterating over a :py:obj:`datetime.date` objects using
:py:obj:`datetime.timedelta` as the step:

.. code-block:: python

    import datetime
    from openrange.date import DateRange

    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=365)
    two_weeks = datetime.timedelta(days=14)

    # yield datetime.date objects for every 2 weeks, starting today, for a year
    for dt_date in DateRange(start_date, end_date, two_weeks):
        # ... profit

**OpenRange** makes implementing these types of classes very simple by
providing an easy-to-use abstract base class called ``BaseRange``.

BaseRange
#########

``BaseRange`` is an abstract base class that provides the common interface for
all **OpenRange** objects. Like the built-in ``range`` object, BaseRange is a
subclass of :py:class:`Sequence<collections.Sequence>` and supports all of the
common sequence operations.

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
        

For example, to implement a ``datetime.date`` range, ``_item_to_num`` would
convert a ``datetime.date`` item to a numerical representation such as seconds
since the epoch. Conversly, ``_num_to_item`` would convert seconds since the
epoch to a ``datetime.date`` object. Once these two are implemented, everything
else is handled by the ``BaseRange`` base class implementation.

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

In the ``datetime.date`` example, the ``step`` might be implemented as a
:py:obj:`datetime.timedelta` object. The ``_step_to_num`` method would convert
the ``datetime.timedelta`` object to seconds whereas ``_num_to_step`` would
convert seconds back to a ``datetime.timedelta`` object.

The default implementations of these ``step`` conversion methods assume the
``step`` is of the same type as ``start`` and ``stop``, and therefore fall back
to calling the ``_item_to_num`` and ``_num_to_item`` methods. 

.. note::

    Unlike the built-in ``range``, ``BaseRange`` implements iteration as
    inclusive of the ``stop`` value. The built-in ``range`` is exclusive of the
    ``stop`` value because it is commonly used to generate integers for
    zero-based indexing of lists. The typical usage of ``BaseRange`` will
    likely not be to generate integer types and so the decision was made to
    make the iteration inclusive of the ``stop`` value.

Full implementation
===================



Support
#######

API
###


Installation
############

Contribute
##########

.. toctree::
    :maxdepth: 3
    :hidden:

    self
    examples
    features
    api

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

