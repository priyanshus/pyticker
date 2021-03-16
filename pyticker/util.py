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


class PyTickerDBOperations(object):
    def __init__(self):
        self._pyticker_db_dir = os.path.join(str(Path.home()), '.pyticker')
        self._db_file_path = os.path.join(self._pyticker_db_dir, 'pyticker.db')

    def init_db(self):
        if not os.path.exists(self._pyticker_db_dir):
            os.mkdir(self._pyticker_db_dir)

            with closing(sqlite3.connect(self._db_file_path)) as connection:
                connection.execute('CREATE TABLE watchlist(symbol TEXT PRIMARY KEY)')
                connection.commit()

    def add_symbol_in_watchlist(self, symbols):
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            try:
                connection.executemany('INSERT INTO watchlist VALUES (?)', symbols)
                connection.commit()
            except sqlite3.IntegrityError:
                pass

    def get_watchlist_symbols(self):
        watchlist_symbols = []
        # TODO Optimize this piece of code as it makes connection in every thread.
        # As salite does not allow to resue the same connection in non-originating threads.
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            for row in connection.execute('SELECT * from watchlist').fetchall():
                for member in row:
                    watchlist_symbols.append(member)

        return ','.join(watchlist_symbols)

    def delete_symbol_in_watchlist(self, symbol):
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            try:
                connection.executemany("DELETE FROM watchlist where symbol = ?", symbol)
                connection.commit()
            except sqlite3.IntegrityError:
                pass

    def close_connection(self):
        self._connection.close()

