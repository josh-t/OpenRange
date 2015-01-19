"""An API for storing and managing frame numbers."""

# ----------------------------------------------------------------------------
# imports:
# ----------------------------------------------------------------------------

from copy import deepcopy
from itertools import count, groupby
from numbers import Number
import re

# ----------------------------------------------------------------------------
# globals:
# ----------------------------------------------------------------------------

# Optionally signed integer for floating point number
FRAME_SPEC = "-?\d*\.?\d*"

# Frame range specification. Can be a single frame or a range of frames
# indicated by the '-' separator. An optional step can also be supplied.
FRANGE_REGEX = re.compile("^({f})(-?({f})(:({f}))?)?$".format(f=FRAME_SPEC))

# A separator regex for parsing a list of frame range specifications
SPEC_SEPARATOR_REGEX = re.compile("\s*,\s*")

# ----------------------------------------------------------------------------
# classes:
# ----------------------------------------------------------------------------
class Frange(object):
    """Stores an ordered list of frame numbers, specified as ranges."""

    separator = ','

    # ------------------------------------------------------------------------
    # special methods:
    # ------------------------------------------------------------------------
    def __add__(self, other):
        new_frange = Frange(list(self._segments))
        new_frange.add(other) 
        return new_frange

    # ------------------------------------------------------------------------
    def __init__(self, frames_arg=None, separator=None):

        self._segments = []
        self._separator = separator \
            if separator is not None else self.__class__.separator
        if frames_arg:
            self.add(frames_arg)

    # ------------------------------------------------------------------------
    def __iter__(self):
        return self.frames

    # ------------------------------------------------------------------------
    def __str__(self):
        return self._separator.join(
            [segment.spec for segment in self._segments]
        )

    # ------------------------------------------------------------------------
    def __sub__(self, other):
        new_frange = Frange(list(self._segments))
        new_frange.remove(other)
        return new_frange

    # ------------------------------------------------------------------------
    # methods:
    # ------------------------------------------------------------------------
    def add(self, frames_arg):
        segments = _segments_from_arg(frames_arg)
        self._segments.extend(segments)

    # ------------------------------------------------------------------------
    def compact(self):
        self._segments = _segments_from_frames(self.frames)

    # ------------------------------------------------------------------------
    def remove(self, frames_arg):
        updated_segments = []
        segments_to_remove = _segments_from_arg(frames_arg)
        frames_to_remove = list(
            set(_frames_from_segments(segments_to_remove))
        )
        for segment in self._segments:
            new_segments = _FrangeSegment.remove(segment, frames_to_remove)
            if new_segments:
                updated_segments.extend(new_segments)

        self._segments = updated_segments

    # ------------------------------------------------------------------------
    # properties
    # ------------------------------------------------------------------------
    @property
    def continuous(self):
        return len(self._segments) == 1 and self._segments[0].step == 1

    # ------------------------------------------------------------------------
    @property
    def segments(self):
        return [Frange(deepcopy(segment)) for segment in self._segments]

    # ------------------------------------------------------------------------
    @property
    def frames(self):
        frames = []
        for segment in self._segments:
            frames.extend(list(segment))

        return frames

# ----------------------------------------------------------------------------
# private classes:
# ----------------------------------------------------------------------------
class _FrangeSegment(object):

    # ------------------------------------------------------------------------
    # class methods:
    # ------------------------------------------------------------------------
    @classmethod
    def remove(cls, segment, frames_to_remove):

        new_segments = []
        cur_frames = list(segment)
        new_frames = [f for f in cur_frames if not f in frames_to_remove]
        return _segments_from_frames(new_frames)

    # ------------------------------------------------------------------------
    # special methods:
    # ------------------------------------------------------------------------
    def __init__(self, start, stop=None, step=None):
        self._start = start
        self._stop = stop if stop is not None else start
        self._step = step if step is not None else 1

        if not self._step:
            raise ValueError("Invalid step: " + self.spec)

    # ------------------------------------------------------------------------
    def __iter__(self):
        return _range(self.start, self.stop, self.step) 

    # ------------------------------------------------------------------------
    def __str__(self):
        return self.spec

    # ------------------------------------------------------------------------
    # properties:
    # ------------------------------------------------------------------------
    @property
    def spec(self):

        start = str(self.start)
        stop = str(self.stop)
        step = str(self.step)
        
        if start == stop:
            spec = start
        else:
            spec = "{start}-{stop}".format(start=start, stop=stop)
            if step != "1" and step != "1.0":
                spec += ":" + step

        return spec

    # ------------------------------------------------------------------------
    @property
    def start(self):
        return self._start

    # ------------------------------------------------------------------------
    @property
    def step(self):
        return self._step

    # ------------------------------------------------------------------------
    @property
    def stop(self):
        return self._stop

# ----------------------------------------------------------------------------
# private functions:
# ----------------------------------------------------------------------------
def _frames_from_segments(segments):
    
    frames = []
    for segment in segments:
        frames.extend(list(segment))
    return frames

# ----------------------------------------------------------------------------
def _num_from_frame_str(frame_str, default=None):

    if frame_str is None:
        return default

    try:
        num = int(frame_str)
    except ValueError:
        num = float(frame_str)

    return num

# ----------------------------------------------------------------------------
def _range(start, stop, step=1):

    i = start

    if start == stop:
        yield start
    elif stop > start:
        while i <= stop:
            yield i
            i += step
    else:
        while i >= stop:
            yield i
            i += step

# ----------------------------------------------------------------------------
def _segments_from_arg(frames_arg):

    segments = []

    # Frange argument
    if isinstance(frames_arg, Frange):
        segments.extend([deepcopy(s) for s in frames_arg._segments])

    # frange segment 
    elif isinstance(frames_arg, _FrangeSegment):
        segments.append(deepcopy(frames_arg))

    # string spec
    elif isinstance(frames_arg, basestring):
        segments.extend(_segments_from_spec(frames_arg))

    # number
    elif isinstance(frames_arg, Number):
        segments.append(_FrangeSegment(frames_arg))

    # list of one of the above?
    else:
        for arg in frames_arg:
            segments.extend(_segments_from_arg(arg))
        
    return segments

# ----------------------------------------------------------------------------
def _segments_from_frames(frames):

    # eliminate duplicates
    frames = sorted(list(set(frames)))

    # calculate all possible steps between the frames
    steps = [frames[f] - frames[f-1] for f in range(1, len(frames))]

    segments = []

    # for each step, in order...
    for step in set(steps):
            
        segments_found = True

        while segments_found:
    
            num_segments = 0

            # segment the frames based on their offset from a matching stepped
            # count. str() to allow floating point differences to segment
            for key, group in groupby(
                frames, lambda f,c=count(step=step): str(next(c)-f)):

                # only count ranges of 3 or more frames
                segment_frames = list(group)

                if len(segment_frames) > 2:
                    num_segments += 1
                    segments.append(_FrangeSegment(
                        segment_frames[0], 
                        stop=segment_frames[-1], 
                        step=step)
                    )
                    for f in segment_frames:
                        frames.remove(f)

            segments_found = True if num_segments > 0 else False

    for frame in frames:
        segments.append(_FrangeSegment(frame))

    return sorted(segments, key=lambda f:f.start)

# ----------------------------------------------------------------------------
def _segments_from_spec(spec):

    segments = []

    for segment_str in SPEC_SEPARATOR_REGEX.split(spec):
        match = FRANGE_REGEX.match(segment_str)
        if match:
            start = _num_from_frame_str(match.group(1))
            stop = _num_from_frame_str(match.group(3), default=start)
            step = _num_from_frame_str(match.group(5), default=1)
            segments.append(_FrangeSegment(start, stop=stop, step=step))
        else:
            raise SyntaxError(
                "Unable to parse segment specification: '{s}'".\
                    format(s=segment_str)
            )

    return segments
        
# ----------------------------------------------------------------------------
if __name__ == "__main__":

    f1 = Frange()
    assert str(f1) == ""
    assert f1.continuous == False
    assert f1.frames == []
    print str(f1)

    f2 = Frange("1.0-2.5:.5")
    assert str(f2) == "1.0-2.5:0.5"
    assert f2.continuous == False
    assert f2.frames == [1.0, 1.5, 2.0, 2.5]
    print str(f2)

    f3 = Frange("10-30:2")
    assert str(f3) == "10-30:2"
    assert f3.continuous == False
    assert f3.frames == [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    print str(f3)

    f4 = Frange("1-50:2,25-75:2", separator=", ")
    print str(f4)
    f4.compact()
    print str(f4)

    f5 = Frange("1-100")
    assert f5.continuous == True
    print str(f5)

    f6 = Frange([1, 2, "1-10:3", "-10-20:5", Frange("11-33:11"), "2.4-9.6:2.4"])
    print str(f6)
    print str(f6.frames)

    f7 = f5 - f3
    print str(f7)
    for f in f7.segments:
        print str(f)
    
    #f8 = Frange("0-100:10,0-100:5,0-100:1")
    #print str(f8)
    #print str(f8.frames)
    #f8.compact()
    #print str(f8.frames)

