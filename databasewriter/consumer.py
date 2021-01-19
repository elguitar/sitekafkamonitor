import json

from kafka import KafkaConsumer

import options

consumer = KafkaConsumer(options.kafka_topic,
                bootstrap_servers=f"{options.kafka_host}:{options.kafka_port}",
                client_id = "dbwriter-1",
                group_id = "dbwriter-group",
                value_deserializer=lambda v: json.loads(v),
                security_protocol="SSL",
                ssl_cafile=".secrets/ca.pem",
                ssl_certfile=".secrets/service.cert",
                ssl_keyfile=".secrets/service.key",
           )
