import pytest
import csv
from datetime import datetime
import os

from weather_pattern import TemperatureData, BadDataException

# TODO: I would like to add a lot more negative test cases to handle all the corner cases

@pytest.fixture
def test_data_path():
    parent_dir = os.path.abspath(os.path.dirname(__file__))
    relpath = "./test_data.csv"
    abspath = os.path.join(parent_dir, relpath)
    return abspath

# +ve test cases
def test_load_csv(test_data_path):
    # SETUP
    t_data = TemperatureData()

    # RUN
    t_data.load_data(test_data_path)

    # ASSERT
    assert len(t_data.dataset.keys()) == 4

def test_lowest_temperature(test_data_path):
    # SETUP
    t_data = TemperatureData()

    t_data.load_data(test_data_path)

    # RUN and ASSERT
    assert t_data.get_lowest_temperature()['station_id'] == '68'

def test_get_fluctuation_across_all_dates(test_data_path):
    # SETUP
    t_data = TemperatureData()
    t_data.load_data(test_data_path)

    # RUN and ASSERT
    assert t_data.get_fluctuation_across_all_dates()[0] == '68'

def test_get_fluctuation_for_date_range(test_data_path):
    # SETUP
    t_data = TemperatureData()
    t_data.load_data(test_data_path)

    # RUN and ASSERT
    assert t_data.get_fluctuation_for_date_range(datetime.strptime("2003.125", "%Y.%f"), datetime.strptime("2003.375", "%Y.%f"))[0] == '81'

# -ve test cases

def test_verify_appropriate_error_when_header_not_present(monkeypatch, test_data_path):
    # SETUP
    def mock_reader(*args, **kwargs):
        print("called me!!")
        return [["68","2000.375","12","22"]]
    monkeypatch.setattr(csv, "reader", mock_reader)

    t_data = TemperatureData()

    # RUN and ASSERT
    with pytest.raises(BadDataException) as e:
        t_data.load_data(test_data_path)

def test_verify_no_exception_when_daterange_not_present(test_data_path):
    # SETUP
    t_data = TemperatureData()
    t_data.load_data(test_data_path)

    # RUN and ASSERT
    assert t_data.get_fluctuation_for_date_range(datetime.strptime("2033.125", "%Y.%f"),
                                                 datetime.strptime("2033.375", "%Y.%f"))[0] == None
