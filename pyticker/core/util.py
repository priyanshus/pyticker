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





