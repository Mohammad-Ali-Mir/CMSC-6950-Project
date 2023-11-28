import numpy as np


def iqr(list=[], scale=1.5):

    q1 = np.quantile(list, 0.25)
    q3 = np.quantile(list, 0.75)
    iqr = q3-q1
    low_lim = q1 - scale*iqr
    high_lim = q3 + scale*iqr

    return low_lim, high_lim
