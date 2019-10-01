from werkzeug.exceptions import abort
from weathertracker.measurement_store import query_measurements


def calculateMetricStats(query_measurement, metric, stat):
   values = []

   for measurement in query_measurement:
      values.append(measurement.metrics[metric])

   if stat=="min":
      value = min(values)
   elif stat == "max":
      value = max(values)
   elif stat == "average":
      value = sum(values)/len(values)

   return({
      'metric': metric,
      'stat': stat,
      'value': value
   })

def get_stats(stats, metrics, from_datetime, to_datetime):

   statistics = []
   query_measurement = query_measurements(from_datetime, to_datetime)

   for metric in metrics:
         for stat in stats:
            result = calculateMetricStats(query_measurement, metric, stat)
            statistics.add(result)

   return statistics
