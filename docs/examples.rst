
Example classes
###############

**OpenRange** comes pre-packaged with some example implementations of custom
arithmetic progression objects using ``BaseRange``.

Range
=====

``Range`` is a generic numerical range implementation. It accepts any of
numerical value (int, float, decimal.Decimal, etc.) for the ``start``,
``stop``, and ``step`` args. The usage and defaults match the built-in
``range``. Iteration yields :py:obj:`float` or :py:obj:`int` objects depending
on the value.

``datetime`` Examples
=====================

**OpenRange** implements 3 range-like objects based on types defined in the
:py:obj:`datetime` module:

DateRange
---------

Generate ``datetime.date`` objects between the given start and stop
``datetime.date`` objects with a ``datetime.timedelta`` step.

DatetimeRange
-------------

Generate ``datetime.datetime`` objects between the given start and stop
``datetime.datetime`` objects with a ``datetime.timedelta`` step.

TimeRange
---------

Generate ``datetime.time`` objects between the given start and stop
``datetime.time`` objects with a ``datetime.timedelta`` step.

.. toctree::
    :maxdepth: 3
    :hidden:

