import json

from kafka import KafkaProducer

import options

producer = KafkaProducer(
               bootstrap_servers=options.kafka_host,
               value_serializer=lambda v: json.dumps(v).encode('utf-8')
           )

default_topic = options.kafka_topic
