
__all__ = [
    'built_in_range',
]

# ----------------------------------------------------------------------------

try:
    built_in_range = xrange
except NameError:
    built_in_range = range

