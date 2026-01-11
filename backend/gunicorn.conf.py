import os

from prometheus_client import start_http_server


bind = f"0.0.0.0:{os.environ["API_PORT"]}"

workers = 4

preload = True

# separate metrics from app so only app needs to be exposed

on_starting = lambda _: start_http_server(int(os.environ["METRICS_PORT"]))
