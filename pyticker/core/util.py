import time
import os
from pathlib import Path
import sqlite3
from contextlib import closing


class ProjectConstants(object):
    WIDTH = 12


def every(delay, task):
    while True:
        task()
        time.sleep(delay)


def create_pyticker_dir() -> str:
    pyticker_dir = os.path.join(str(Path.home()), '.pyticker')

    if not os.path.exists(pyticker_dir):
        os.mkdir(pyticker_dir)

    return pyticker_dir
