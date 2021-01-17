"""Commonly used options for the databasewriter"""
import os

from dotenv import load_dotenv

load_dotenv()

kafka_host = os.getenv("KAFKA_HOST")
kafka_port = os.getenv("KAFKA_PORT")
kafka_topic = os.getenv("KAFKA_TOPIC")

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

table_name = "measurements"

poll_interval = 1 
