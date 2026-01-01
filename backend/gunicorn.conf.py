import os


bind = f"0.0.0.0:{os.environ["API_PORT"]}"

workers = 4

preload = True
