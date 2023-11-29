import pytest
import functions
# from functions import *


@pytest.mark.parametrize("data, scale, limits", [
    ([-20, -2, 0, 1, 2, 20], [], [-6.375, 6.625]),  # scale=1.5
    ([-20, -2, 0, 1, 2, 20], 1.5, [-6.375, 6.625]),
    ([-20, -2, 0, 1, 2, 20], 2, [-8, 8.25]),  # scale=2
    ([-20, -2, 0, 1, 2, 20], -1, [-6.375, 6.625]),
    ([0], [], [0, 0]),
    ([], [], None),
    (['a', 'b', 'c'], [], None),
    (functions.pd.Series([1, 2, 3, 4, 5]), [], [-1, 7])  # Series
])
def test_iqr_limits(data, scale, limits):
    result = functions.iqr_limits(data, scale)
    assert result == limits


@pytest.mark.parametrize("data, history_data, sensitivity,\
                         extremes_values, extremes_indexes", [
    ([5, 10, 3, 0, -10, 20], [6, 9, 1, 2, 5.5, 4], 10, [-10, 20], [4, 5]),
    ([5, 10, 3, 0, -10, 20], [6, 9, 1, 2, 5.5, 4], None, [-10, 20], [4, 5]),
    # sensitivity: default
    ([5, 10, 3, 0, -10, 20], [6, 9, 1, 2, 5.5, 4], -10, [-10, 20], [4, 5]),
    # sensitivity: negative
    ([5, 10, 3, 0, -10, 20], [], None, None, None),
    ([], [6, 9, 1, 2, 5.5, 4], None, None, None),
    ([5, 10, 3, 0, 0, 9.5, 10], [6, 9, 1, 2, 5.5, 4, 10], 5, [0, 9.5], [4, 5]),
    # sensitivity: five
    ([0, 10, 15, 20, 5], [6, 12, 10, 14, 9], 5, [0, 20], [0, 3]),
    ([0], [6], 5, [0], [0])
])
def test_historical_extremes(data, history_data, sensitivity,
                             extremes_values, extremes_indexes):
    result = functions.historical_extremes(data, history_data, sensitivity)
    expected = functions.pd.Series(extremes_values, extremes_indexes,
                                   dtype='float64')
    assert result.equals(expected)
###################################################################
# python -m pytest -v test_functions.py::test_historical_extremes
