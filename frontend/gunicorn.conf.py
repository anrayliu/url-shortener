import os


bind = f"0.0.0.0:{os.environ["WEB_PORT"]}"

workers = 4

preload = True
