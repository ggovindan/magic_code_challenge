import csv
from collections import defaultdict
from datetime import datetime
import statistics
import functools
import time


class BadDataException(Exception):
    pass

def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start = time.perf_counter()
        value = func(*args, **kwargs)
        end = time.perf_counter()
        run_time = end - start
        print(f"{func.__name__} execution_time: {run_time:.4f} secs")
        return value
    return wrapper_timer

class TemperatureData:
    """
    This class represents the dataset imported from CSV file
    The following shows how the data is represented inside `dataset` attribute of this class
    {
     "1": {
            "records": [{"station_id": "1", "temp_c": 12.33, "date": datetime.datetime(2020, 1, 1, 0, 0, 0, 542000)},
                       {"station_id": "1", "temp_c": 11.33, "date": datetime.datetime(2020, 1, 1, 0, 0, 0, 667000)}]
            "min_recorded_temp": 11.33,
            "min_recorded_date": datetime.datetime(2020, 1, 1, 0, 0, 0, 667000),
            "max_recorded_date": datetime.datetime(2020, 1, 1, 0, 0, 0, 542000),
            "max_recorded_temp": 12.33
        }
    }
    """

    def __init__(self):
        self.dataset = defaultdict(dict)
        self.last_seen_lowest = None
        self.last_seen_max_fluctuation = None
        # some timestamps to avoid processing the same calculation if the data has not changed
        self.last_update_time = datetime.utcfromtimestamp(0)
        self.last_import_time = datetime.utcfromtimestamp(0)

    @timer
    def load_data(self, csv_path: str):
        with open(csv_path) as csvfile:
            csvdata = csv.reader(csvfile, delimiter=",")
            keys = None

            def convert_data(datapoint) -> dict:
                # For easier calculation, assuming the unique id after the year as milliseconds
                datapoint["date"] = datetime.strptime(datapoint["date"], "%Y.%f")
                datapoint["temp_c"] = float(datapoint["temperature_c"])
                return datapoint

            for row in csvdata:
                if "station_id" in row:
                    keys = row
                    continue
                try:
                    data_dict = dict(zip(keys, row))
                except:
                    raise BadDataException("Exception: header missing or columns do not match for csvheader={} row={}".format(keys, row))


                station_id = data_dict["station_id"]
                if not self.dataset.get(station_id):
                    converted_data = convert_data(data_dict)
                    self.dataset[station_id] = {"records": [converted_data],
                                                "min_recorded_temp": converted_data['temp_c'],
                                                "max_recorded_temp": converted_data['temp_c'],
                                                "min_recorded_date": converted_data['date'],
                                                "max_recorded_date": converted_data['date']}
                else:
                    converted_data = convert_data(data_dict)
                    self.dataset[station_id]["records"].append(converted_data)
                    if converted_data['temp_c'] < self.dataset[station_id]["min_recorded_temp"]:
                        self.dataset[station_id]["min_recorded_temp"] = converted_data['temp_c']
                        self.dataset[station_id]["min_recorded_date"] = converted_data['date']
                    if converted_data['temp_c'] > self.dataset[station_id]["max_recorded_temp"]:
                        self.dataset[station_id]["max_recorded_temp"] = converted_data['temp_c']
                        self.dataset[station_id]["max_recorded_date"] = converted_data['date']

            self.last_import_time = datetime.utcnow()

    # Part 1:
    @timer
    def get_lowest_temperature(self):
        if self.last_import_time < self.last_update_time:
            return self.last_seen_lowest

        self.last_seen_lowest = min([{"station_id": k, "date": v["min_recorded_date"], "min_temp": v["min_recorded_temp"]} \
                                     for k, v in self.dataset.items()], key=lambda x: x["min_temp"])
        return self.last_seen_lowest

    # Part 2;
    @timer
    def get_fluctuation_across_all_dates(self):
        variance_per_station = {}
        for station_id in self.dataset:
            try:
                variance_per_station[station_id] = statistics.variance([v['temp_c'] for v in self.dataset[station_id]['records']])
            except statistics.StatisticsError:
                # if it cant find entries in the date range for a station skip it
                pass
        return max([(k,v) for k,v in variance_per_station.items()], key=lambda x: x[1])

    # part 3:
    @timer
    def get_fluctuation_for_date_range(self, start_dt, end_dt):
        variance_per_station = {}
        for station_id in self.dataset:
            try:
                variance_per_station[station_id] = statistics.variance([v['temp_c'] for v in self.dataset[station_id]['records'] if start_dt <= v["date"] <= end_dt])
            except statistics.StatisticsError:
                # if it cant find entries in the date range for a station skip it
                pass

        if len(variance_per_station.keys()) == 0:
            # none of the stations have data for the specified date range
            return (None, None)
        return max([(k, v) for k, v in variance_per_station.items()], key=lambda x: x[1])


if __name__ == "__main__":
    obj = TemperatureData()
    obj.load_data("../data.csv")
    print(obj.get_lowest_temperature())
    print(obj.get_fluctuation_across_all_dates())
    print(obj.get_fluctuation_for_date_range(datetime.strptime("2003.125", "%Y.%f"), datetime.strptime("2003.375", "%Y.%f")))
