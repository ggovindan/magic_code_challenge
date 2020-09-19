
import pytest
from flatten_array import flatten_array


def test_empty_array():
    # SETUP
    values = []
    result = []

    # RUN
    flatten_array(values, result)

    # Assert
    assert len(result) == 0


def test_single_dimension():
    # SETUP
    values = [1, 2, 3, 4]
    result = []

    # RUN
    flatten_array(values, result)

    # Assert
    assert len(result) == len(values)


def test_multi_dimensions():
    # SETUP
    values = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12], [13, [14, 15, 16]], [17, 18]]
    result = []

    # RUN
    flatten_array(values, result)

    # Assert
    assert len(result) == 18


def test_multi_dimensions_with_tuples():
    # SETUP
    values = [[1, 2, 3, 4, 5, 6, 7, 8, 9], (10, 11, 12), [13, [14, 15, 16]], [17, 18]]
    result = []

    # RUN
    flatten_array(values, result)

    # Assert
    assert len(result) == 18


def test_empty_arrays():
    # SETUP
    values = [[], [], []]
    result = []

    # RUN
    flatten_array(values, result)

    # Assert
    assert len(result) == 0


def test_non_array():
    # SETUP
    values = 12
    result = []

    # RUN and exception as assert
    with pytest.raises(TypeError):
        flatten_array(values, result)
