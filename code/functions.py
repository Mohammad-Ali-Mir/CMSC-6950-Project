import numpy as np
import pandas as pd


def iqr_limits(data=[], scale=1.5):
    if isinstance(data, pd.Series):
        data = data.tolist()  # Convert Series to list
    if len(data) == 0:
        return None
    if not isinstance(scale, (float, int)) or scale < 0:
        scale = 1.5

    try:
        q1 = np.quantile(data, 0.25)
        q3 = np.quantile(data, 0.75)
        iqr = q3 - q1
        low_lim = q1 - scale * iqr
        high_lim = q3 + scale * iqr
        limits = [low_lim, high_lim]
        return limits
    except Exception:
        return None


def historical_extremes(data, history_data, sensitivity=10):
    if len(data) == 0 or len(history_data) == 0:
        return pd.Series(None, None, dtype='float64')
    if not isinstance(sensitivity, (float, int)) or sensitivity < 0:
        sensitivity = 10
    if sensitivity < 0:
        sensitivity = -sensitivity
    if isinstance(data, list):
        data = pd.Series(data)
    if isinstance(history_data, list):
        history_data = pd.Series(history_data)

    flags = np.where((data < history_data - sensitivity) |
                     (data > history_data + sensitivity),
                     'Extreme', 'Normal')

    extreme_indices = np.where(flags == 'Extreme')[0]
    extreme_data = data[extreme_indices]

    return extreme_data.astype('float')
################################################
