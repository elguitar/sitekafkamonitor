import json

from kafka import KafkaProducer

import options

producer = KafkaProducer(
               bootstrap_servers=f"{options.kafka_host}:{options.kafka_port}",
               value_serializer=lambda v: json.dumps(v).encode('utf-8'),
               security_protocol="SSL",
               ssl_cafile=options.root_path / ".secrets/ca.pem",
               ssl_certfile=options.root_path / ".secrets/service.cert",
               ssl_keyfile=options.root_path / ".secrets/service.key"
           )

default_topic = options.kafka_topic
