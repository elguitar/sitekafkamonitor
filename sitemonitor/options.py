"""Commonly used options for the sitemonitor"""
import pathlib
import os

from dotenv import load_dotenv

load_dotenv()

kafka_host = os.getenv("KAFKA_HOST")
kafka_port = os.getenv("KAFKA_PORT")
kafka_topic = os.getenv("KAFKA_TOPIC")

root_path = pathlib.Path(__file__).parent
sleeptime = 1  # Seconds
