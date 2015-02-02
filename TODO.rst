base
----
* add union/intersection method for Range
* make abc for all Range objects
  ** only really have to implement conversion methods 
  ** that's all current subclasses do anyway
* add enumerate to all range objects
* exclude option
* make repeat/exclude part of the range specification
* a method on RangeList to iterate over subranges simultaneously and 
  return a tuple of all the values. Zip like.

date/time
---------

* Add TimeRange. 
  ** Limit TimeRange start/stop 0-23:59:59 (in seconds)
  ** Default step is 1h
  ** Make date/time base class more generic?
* figure out date/time range strings

funcs
-----
* a range based decorator. 
  ** Could be useful for iterating over a test case with various values. 

new
---
  * make a RangeDict object

other
-----
* register in PyPI
* get running on travis ci
* full test coverage
* full pydoc coverage
* sphinx docs on RTD
* finish README

