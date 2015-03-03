
########
Examples
########

Here are some example classes that come pre-packaged with **OpenRange**.

.. toctree:: 
    :maxdepth: 2

DateRange
^^^^^^^^^

Generate ``datetime.date`` objects between the given start and stop
``datetime.date`` objects with a ``datetime.timedelta`` step.

.. code-block:: python
    :emphasize-lines: 6

    from datetime import date, timedelta
    from openrange import DateRange
    today = date.today()
    two_weeks = today + timedelta(days=14)
    every_four_days = timedelta(days=4)
    [d for d in DateRange(today, two_weeks, every_four_days)]
    # [datetime.date(2015, 2, 27), datetime.date(2015, 3, 3), datetime.date(2015, 3, 7), datetime.date(2015, 3, 11)]

DatetimeRange
^^^^^^^^^^^^^

Generate ``datetime.datetime`` objects between the given start and stop
``datetime.datetime`` objects with a ``datetime.timedelta`` step.

.. code-block:: python
    :emphasize-lines: 6

    from datetime import datetime, timedelta
    from openrange import DatetimeRange
    now = datetime.now()
    three_days = now + timedelta(days=3)
    every_18_hours = timedelta(hours=18)
    [dt for dt in DatetimeRange(now, three_days, every_18_hours)]
    # [datetime.datetime(2015, 2, 27, 20, 11, 36), datetime.datetime(2015, 2, 28, 14, 11, 36), datetime.datetime(2015, 3, 1, 8, 11, 36), datetime.datetime(2015, 3, 2, 2, 11, 36), datetime.datetime(2015, 3, 2, 20, 11, 36)]

TimeRange
^^^^^^^^^

Generate ``datetime.time`` objects between the given start and stop
``datetime.time`` objects with a ``datetime.timedelta`` step.

XXX

Range
^^^^^

Inclusive, generic numerical range that supports int, float ,and decimal types
for any of start, stop, and step. Usage is identical to python's built-in 
``range()``.

XXX


