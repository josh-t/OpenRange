"""
TODO: 

count()
- ordered

"""

# ----------------------------------------------------------------------------
# imports:
# ----------------------------------------------------------------------------

from itertools import count, groupby
import re

# ----------------------------------------------------------------------------
# globals:
# ----------------------------------------------------------------------------

FRAME_SPEC = "-?\d*\.?\d*"
FRANGE_REGEX = re.compile(
    "^({int})(-?({int})(:({int}))?)?$".format(int=FRAME_SPEC)
)

# ----------------------------------------------------------------------------
# classes:
# ----------------------------------------------------------------------------
class Frange(object):

    separator = ","

    # ------------------------------------------------------------------------
    # special methods:
    # ------------------------------------------------------------------------
    def __add__(self, other):
        new_frange = Frange(self.frames)
        new_frange.add(other) 
        return new_frange

    # ------------------------------------------------------------------------
    def __init__(self, frames_arg, frame_type=int):
        self._frames = set()
        self._frame_type = frame_type
        self.add(frames_arg)

    # ------------------------------------------------------------------------
    def __iter__(self):
        return iter(self.frames)

    # ------------------------------------------------------------------------
    def __str__(self):
        return _frames_to_spec(self.frames)

    # ------------------------------------------------------------------------
    def __sub__(self, other):
        new_frange = Frange(self.frames)
        new_frange.remove(other)
        return new_frange

    # ------------------------------------------------------------------------
    # methods:
    # ------------------------------------------------------------------------
    def add(self, frames_arg):
        frames_to_add = _frames_from_arg(
            frames_arg, 
            frame_type=self.frame_type
        )
        self._frames |= set(frames_to_add)

    # ------------------------------------------------------------------------
    def remove(self, frames_arg):
        frames_to_remove = _frames_from_arg(
            frames_arg, 
            frame_type=self.frame_type
        )
        self._frames = self._frames.difference(frames_to_remove)

    # ------------------------------------------------------------------------
    # properties: 
    # ------------------------------------------------------------------------
    @property
    def continuous(self):
        segments = _frames_to_segments(self._frames)
        return len(segments) == 1 and segments[0].step == 1

    # ------------------------------------------------------------------------
    @property
    def frame_type(self):
        return self._frame_type

    # ------------------------------------------------------------------------
    @property
    def frames(self):
        return sorted(list(self._frames))

    # ------------------------------------------------------------------------
    @property
    def subfranges(self):
        for segment in _frames_to_segments(self.frames):
            yield Frange(segment.frames)

# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
class _FrameSegment(object):

    # ------------------------------------------------------------------------
    def __init__(self, frames, step):
        self._frames = frames
        self._step = step

    # ------------------------------------------------------------------------
    @property
    def frames(self):
        return self._frames

    # ------------------------------------------------------------------------
    @property
    def step(self):
        return self._step

# ----------------------------------------------------------------------------
# funcitons
# ----------------------------------------------------------------------------
def _frames_from_arg(frames_arg, frame_type=int):

    if isinstance(frames_arg, Frange):
        frames = frames_arg.frames
    elif isinstance(frames_arg, basestring):
        frames = _spec_to_frames(frames_arg, frame_type=frame_type)
    else:
        frames = frames_arg

    return frames

# ----------------------------------------------------------------------------
def _frames_to_segments(frames):

    # eliminate duplicates
    frames = sorted(list(set(frames)))

    # calculate all possible steps between the frames
    steps = [frames[f] - frames[f-1] for f in _range(1, len(frames))]

    segments = []

    # for each step, in order...
    for step in set(steps):
            
        segments_found = True

        while segments_found:
    
            num_segments = 0

            # segment the frames based on their offset from a matching stepped count
            # str() to allow float differences to segment
            for key, group in groupby(frames, lambda f,c=count(step=step): str(next(c)-f)):

                # only count ranges of 3 or more frames
                segment_frames = list(group)

                if len(segment_frames) > 2:
                    num_segments += 1
                    segments.append(_FrameSegment(segment_frames, step))
                    for f in segment_frames:
                        frames.remove(f)

            segments_found = True if num_segments > 0 else False

    for frame in frames:
        segments.append(_FrameSegment([frame], 1))

    return sorted(segments, key=lambda f:f.frames[0])

# ----------------------------------------------------------------------------
def _frames_to_spec(frames, separator=Frange.separator):

    segments = _frames_to_segments(frames)

    frange_list = []
    for segment in segments:

        frames = segment.frames
        step = segment.step

        if len(frames) == 1:
            frange_list.append(str(frames[0]))
        else:
            frange_str = "{b}-{e}".format(b=frames[0], e=frames[-1])
            if step != 1:
                frange_str += ":" + str(step)
            frange_list.append(frange_str) 

    return separator.join(frange_list)

# ----------------------------------------------------------------------------
def _range(start, stop, step=1):

    i = start
    if stop > start:
        while i < stop:
            yield i
            i += step
    else:
        while i >= stop:
            yield i
            i += step

# ----------------------------------------------------------------------------
def _spec_to_frames(specs, frame_type=int, separator=Frange.separator):

    frames = []

    for spec in specs.split(separator):
        match = FRANGE_REGEX.match(spec)
        if match:
            start = match.group(1)
            stop = match.group(3)
            step = match.group(5)
            if None in (stop, step):
                if stop is None:
                    frames.append(frame_type(start))
                else:
                    frames.extend(_range(frame_type(start), frame_type(stop) + 1))
            else:
                frames.extend(_range(frame_type(start), frame_type(stop), frame_type(step)))
        else:
            raise SyntaxError(
                "Unable to parse frame specification: '" + str(spec) + "'"
            )

    return frames
    

# -------------

frames = [
    -4, -2, 0, 3, 5, 7, 9, 12, 14, 15, 16, 17, 18, 21, 26, 31, 36, 41, 100, 200, 300,
    400, 599, 47,
]

f1 = Frange(frames)
print "FRANGE: " + str(f1)

f2 = Frange("1-100")
print "FRANGE: " + str(f2)

f3 = f2 + f1
print "FRANGE: " + str(f3)

f4 = Frange([1.3, 2.6, 3.9, 4.2, 5, 6, 7, 8, 19.1, 19.2, 19.3, 19.4], frame_type=float)
print "FRANGE: " + str(f4)

f5 = Frange("10-0:-1")
print "FRANGE: " + str(f5)

f6 = Frange("-10.5--20.5:-.5", frame_type=float)
print "FRANGE: " + str(f6)

