# Extended Cascade stdlib: robust and production-quality.
# All functions have clear docstrings.

import math
import random
import time
from functools import reduce

def flow(value, destination=None):
    """Print value to output. Destination can be 'console' or None (default stdout)."""
    if destination == "console" or destination is None:
        print(value)

def measure(value):
    """Return length of a list, string, or dict."""
    if isinstance(value, (list, str, dict)):
        return len(value)
    raise TypeError("measure() expects list, string, or map")

def filter_basin(basin, predicate):
    """Return a filtered list using the predicate function."""
    return [x for x in basin if predicate(x)]

def map_basin(basin, func):
    """Apply func to each item in basin (list)."""
    return [func(x) for x in basin]

def reduce_basin(basin, func, initial):
    """Reduce basin with func and initial value."""
    return reduce(func, basin, initial)

def to_rivulet(value):
    """Convert value to string."""
    return str(value)

def to_depth(value):
    """Convert value to float."""
    try:
        return float(value)
    except Exception:
        raise TypeError("Cannot convert to depth")

def to_drop(value):
    """Convert value to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "yes", "1")
    return bool(value)

def random_depth():
    """Return a random float in [0, 1)."""
    return random.random()

def now():
    """Return the current Unix timestamp (float)."""
    return time.time()

def sort_basin(basin):
    """Return a sorted copy of basin (list)."""
    return sorted(basin)

def max_basin(basin):
    """Return the max value of basin (list)."""
    return max(basin)

def min_basin(basin):
    """Return the min value of basin (list)."""
    return min(basin)

def sum_basin(basin):
    """Return the sum of basin (list)."""
    return sum(basin)

def avg_basin(basin):
    """Return the average of basin (list). Returns 0 for empty list."""
    if not basin:
        return 0
    return sum(basin) / len(basin)

def abs_depth(value):
    """Return the absolute value of a number."""
    return abs(value)

def sqrt_depth(value):
    """Return the square root of a number."""
    return math.sqrt(value)

def log_depth(value, base=math.e):
    """Return the logarithm of value to given base."""
    return math.log(value, base)

def pow_depth(x, y):
    """Return x raised to the power of y."""
    return math.pow(x, y)

def upper_rivulet(s):
    """Return an upper-cased string."""
    return str(s).upper()

def lower_rivulet(s):
    """Return a lower-cased string."""
    return str(s).lower()

def strip_rivulet(s):
    """Return string with leading/trailing whitespace removed."""
    return str(s).strip()

def split_rivulet(s, sep=None):
    """Split string by separator."""
    return str(s).split(sep)

def join_basin(basin, sep=""):
    """Join list of strings with separator."""
    return sep.join(map(str, basin))