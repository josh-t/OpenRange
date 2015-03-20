
.. toctree::
    :maxdepth: 2
    :hidden:

    self
    docs
    api

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
numerically. For example, you might be interested in a range-like interface for
iterating over a :py:obj:`datetime.date` objects using
:py:obj:`datetime.timedelta` as the ``step``. **OpenRange** provides an example
implementation that does just that:

.. literalinclude:: ../examples/daterange_usage.py
    :language: python

**OpenRange** makes implementing these types of classes very simple by
providing an easy-to-use abstract base class called ``BaseRange``. See the
full `Documentation <docs.html>`_ for more info.

.. include:: ../README.rst
    :start-after: @divider@

Indices and tables
##################

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

