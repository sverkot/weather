from flask import request, jsonify, Flask, Response
from flask.views import MethodView
from werkzeug.exceptions import abort

from weathertracker import measurement_store
from weathertracker.measurement import Measurement
from weathertracker.measurement_store import add_measurement
from weathertracker.utils.conversion import (
    convert_to_datetime,
    DatetimeConversionException,
)

app = Flask(__name__)


class MeasurementsAPI(MethodView):
    @staticmethod
    def validate_data(data):

        # Check if timestamp exists
        timestamp = data['timestamp']
        if timestamp is None:
            return False

        # Check if the temperature exists it is a float
        temperature = data['temperature']
        if temperature is not None:
            if not isinstance(temperature,float):
                return False

        dewPoint = data['dewPoint']
        if dewPoint is not None:
            if not isinstance(dewPoint,float):
                return False

        # precipitation = data['precipitation']
        # if precipitation is not None:
        #     if not isinstance(precipitation,float):
        #         return False

        return True

    @staticmethod
    def convert_timestamp_to_z(timestamp):

        return timestamp.isoformat().replace('+00:00', '.000Z')

    # features/01-measurements/01-add-measurement.feature
    def post(self):
        data = request.get_json(force=True)
        timestamp = data['timestamp']

        if not self.validate_data(data):
            return abort(400)

        try:
            timestamp = convert_to_datetime(timestamp)
        except DatetimeConversionException:
            return abort(400)

        metrics = {}
        metrics['temperature'] = data['temperature']
        metrics['dewPoint'] = data['dewPoint']
        metrics['precipitation'] = data['precipitation']
        measurement = Measurement(timestamp, metrics)
        measurement_store.add_measurement(measurement)
        result = {
            "timestamp": self.convert_timestamp_to_z(measurement.timestamp),
            "temperature": measurement.metrics['temperature'],
            "dewPoint": measurement.metrics['dewPoint'],
            "precipitation": measurement.metrics["precipitation"]
        }
        response = jsonify(result)
        response.status_code = 201
        response.headers['location'] = '/measurements/' + self.convert_timestamp_to_z(measurement.timestamp)
        return response

        # return Response(status=201)

    # features/01-measurements/02-get-measurement.feature
    def get(self, timestamp):

        try:
            timestamp = convert_to_datetime(timestamp)
        except DatetimeConversionException:
            return abort(400)

        measurement = measurement_store.get_measurement(timestamp)
        if measurement != None:
            result = {
                "timestamp": self.convert_timestamp_to_z(measurement.timestamp),
                "temperature": measurement.metrics['temperature'],
                "dewPoint": measurement.metrics['dewPoint'],
                "precipitation": measurement.metrics["precipitation"]
            }
            response = jsonify(result)
            response.status_code = 201
            response.headers['location'] = '/measurements/' + self.convert_timestamp_to_z(measurement.timestamp)
            return response
            # return jsonify(result), 200
        else:
            return Response(status=404)
