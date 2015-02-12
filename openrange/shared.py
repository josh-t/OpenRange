
__all__ = [
    'built_in_range',
    'first_middle_last',
]

# ----------------------------------------------------------------------------

try:
    built_in_range = xrange
except NameError:
    built_in_range = range

# ----------------------------------------------------------------------------
def first_middle_last(items):
    """Given a list of items, return the first, middle, and last item"""

    num_items = 0
    for i in items:
        if num_items == 0:
            first = i
        last = i
        num_items += 1
    
    # calculate the index of the middle item
    if num_items % 2 == 0:
        middle_idx = int(num_items / 2) -1
    else:
        middle_idx = int(num_items / 2)

    count = 0
    for i in items:
        middle = i
        if count == middle_idx:
            break
        count += 1
        
    return (first, middle, last)
        
