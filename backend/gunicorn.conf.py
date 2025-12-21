import os
import multiprocessing


bind = f"0.0.0.0:{os.environ["API_PORT"]}"

workers = multiprocessing.cpu_count() * 2 + 1

preload = True
