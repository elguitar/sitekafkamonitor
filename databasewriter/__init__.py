import datetime
import time

import consumer
from db import MeasurementPostgresClient as dbclient
import options

class KafkaToDB:
    """ """

    def __init__(self):
        self.consumer = consumer.consumer
        self.poll_interval = options.poll_interval

    def _record_from_response(self, response):
        """ """
        return list(response.values())[0] if response else []

    def _preprocess_records(self, records):
        """ """
        preprocessed = []
        for r in records:
            v = r.value
            preprocessed.append(
                (v['site'],
                 v['status'],
                 v['latency'],
                 v['regex_found'],
                 datetime.datetime.fromtimestamp(r.timestamp / 1000))
            )
        return preprocessed

    def run(self):
        dbclient().create_measurements_table()
        while True:
            response = self.consumer.poll()
            records = self._record_from_response(response)
            preprocessed_records = self._preprocess_records(records)
            if preprocessed_records != []:
                dbclient().batch_insert_measurements(preprocessed_records)
            time.sleep(self.poll_interval)

if __name__ == "__main__":
    ktdb = KafkaToDB()
    ktdb.run()
