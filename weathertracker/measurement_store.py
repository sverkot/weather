from .measurement import Measurement
from werkzeug.exceptions import abort

# global list to store the measurements in memory
measurements = {}


def add_measurement(measurement):
   measurements[measurement.timestamp] = measurement;



def get_measurement(date):
    return measurements.get(date);


def query_measurements(start_date, end_date):
    results = []
    for timestamp in measurements.keys():
        if start_date < timestamp < end_date:
            results.append(measurements[timestamp]);

    return results;
