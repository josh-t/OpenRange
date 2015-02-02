base
----
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

funcs
-----
* a range based decorator. 
  ** Could be useful for iterating over a test case with various values. 

new
---
* an object that identified a range, but you could define named subranges. so 
  you could iterate over the whole thing like a regular Range object, but it 
  would expose the named subranges via properties that were also iterable. if 
  you add/remove a named subrange it may expand overall range of the object. 

other
-----
* register in PyPI
* get running on travis ci
* full test coverage
* full pydoc coverage
* sphinx docs on RTD
* finish README

