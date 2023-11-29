import pytest
import functions


@pytest.mark.parametrize("one,two",
                         [("R2D2", False),
                          # R2D2 is too short
                          ])
def test_functions(data, expected):
    assert functions.iqr_limits(data) == expected
