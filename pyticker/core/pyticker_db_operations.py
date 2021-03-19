import os
import sqlite3
from contextlib import closing
from pathlib import Path


def calculate_new_buy_average(prev_qty, prev_buy_price, added_qty, new_buy_price):
    return round(((prev_qty * prev_buy_price) + (added_qty * new_buy_price)) / (prev_qty + added_qty), 2)


class PyTickerDBOperations(object):
    def __init__(self):
        self._pyticker_db_dir = os.path.join(str(Path.home()), '.pyticker')
        self._db_file_path = os.path.join(self._pyticker_db_dir, 'pyticker.db')

    def init_db(self):
        if not os.path.exists(self._pyticker_db_dir):
            os.mkdir(self._pyticker_db_dir)

            with closing(sqlite3.connect(self._db_file_path)) as connection:
                connection.execute('CREATE TABLE watchlist(symbol TEXT PRIMARY KEY)')
                connection.execute('CREATE TABLE positions(symbol TEXT PRIMARY KEY, qty INTEGER, buy_price INTEGER)')
                connection.commit()

    def add_symbol_in_watchlist(self, symbols):
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            try:
                connection.executemany('INSERT INTO watchlist VALUES (?)', symbols)
                connection.commit()
            except sqlite3.IntegrityError:
                pass

    def get_stock_symobls_to_fetch_quotes(self) -> tuple:
        """
        Get stock symbols to fetch quotes
        :return: list_of_watchlist_stock_symbols, list_of_positions_stock_symbols)
        """
        watchlist_stock_symbols = []
        position_stock_symbols = []
        # TODO Optimize this piece of code as it makes connection in every thread.
        # As salite does not allow to resue the same connection in non-originating threads.
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            for row in connection.execute('SELECT * from watchlist').fetchall():
                watchlist_stock_symbols.append(row[0])

            for row in connection.execute('SELECT * from positions').fetchall():
                position_stock_symbols.append(row[0])

        return watchlist_stock_symbols, position_stock_symbols

    def delete_symbol_in_watchlist(self, symbol):
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            try:
                connection.executemany("DELETE FROM watchlist where symbol = ?", symbol)
                connection.commit()
            except sqlite3.IntegrityError:
                pass

    def add_position(self, position_details):
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            try:
                previous_position = connection.execute('SELECT * FROM positions WHERE symbol = ?',
                                                       (position_details[0],)) \
                    .fetchone()
                if previous_position:
                    new_quantity = previous_position[1] + int(position_details[1])
                    new_average_price = calculate_new_buy_average(previous_position[1], previous_position[2],
                                                                  int(position_details[1]), int(position_details[2]))
                    connection.execute('UPDATE positions SET qty = ?, buy_price = ? where symbol = ?',
                                       (new_quantity, new_average_price, position_details[0]))
                else:
                    connection.execute('INSERT INTO positions VALUES(?,?,?)', position_details)
                connection.commit()
            except sqlite3.IntegrityError:
                pass

    def update_position(self, position_details):
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            try:
                previous_position = connection.execute('SELECT * FROM positions WHERE symbol = ?',
                                                       (position_details[0],)) \
                    .fetchone()
                if previous_position and int(position_details[1]) < previous_position[1]:
                    new_quantity = previous_position[1] - int(position_details[1])
                    connection.execute('UPDATE positions SET qty = ? where symbol = ?',
                                       (new_quantity, position_details[0]))
                elif previous_position and int(position_details[1]) == previous_position[1]:
                    connection.execute('DELETE FROM positions WHERE symbol=?', (position_details[0],))
                else:
                    pass
                connection.commit()
            except sqlite3.IntegrityError:
                pass

    def get_positions(self):
        positions = dict()
        # TODO Optimize this piece of code as it makes connection in every thread.
        # As salite does not allow to resue the same connection in non-originating threads.
        with closing(sqlite3.connect(self._db_file_path)) as connection:
            for row in connection.execute('SELECT * from positions').fetchall():
                positions[row[0]] = {
                    'symbol': row[0],
                    'qty': row[1],
                    'buy_price': row[2]
                }

        return positions


if __name__ == '__main__':
    db = PyTickerDBOperations()
    db.init_db()
    print(db.get_stock_symobls_to_fetch_quotes())
    print(db.get_positions())
