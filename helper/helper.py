"""Helper functions."""

from math import log10
from math import floor


def ffloat(value):
    """Format a floating point value into a nice string."""
    return '%g' % value



def gen_tics(data_min, data_max, step=None, opt_tics=10):
    """Compute and return the tics for the specified value range."""

    vrange = data_max - data_min

    if vrange <= 0:
        raise RuntimeError('Invalid data range: [%f, %f]' % (data_min, data_max))
    
    if step is None:
        lstep = 10 ** floor(log10(vrange/10.0))
        sane_steps = [lstep, 2*lstep, 5*lstep, 10*lstep, 3, 4]
        counts = [int(vrange/sstep) + 1 for sstep in sane_steps]
        costs = [abs(count - opt_tics) for count in counts]
        index = costs.index(min(costs))
        step = sane_steps[index]
        count = counts[index]
    else:
        count = int(vrange/step) + 1

    tics = []
    value = float(data_min)
    all_int = True
    max_decimal = 0
    i = 0
    while value < data_max:
        value = data_min + i * step
        tic = '%g' % value
        if tic.find('e') != -1: 
            tic = '%.2f' % value
        tics.append((value, tic))
        if tic.find('.') != -1:
            all_int = False
            max_decimal = max(max_decimal, len(tic.split('.')[1]))
        i += 1

    if all_int: return tics

    meta = '%%.0%df' % max_decimal
    
    for i, (value, tic) in enumerate(tics):
        tics[i] = (value, meta % value)

    return tics
