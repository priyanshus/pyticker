import os
import pathlib
import unittest

from pyticker.core.pyticker_db_operations import PyTickerDBOperations


class PyTickerDBOperationsTests(unittest.TestCase):

    def setUp(self) -> None:
        self.__file = open(os.path.join(pathlib.Path().absolute(), 'test.db'), "w")
        self.__pydb = PyTickerDBOperations(os.path.join(pathlib.Path().absolute(), 'test.db'))
        self.__pydb.init_db()
        self.__file.close()

    def doCleanups(self) -> None:
        pathlib.Path(os.path.join(pathlib.Path().absolute(), 'test.db')).unlink()

    def test_fetch_stock_symbols_for_watchlist(self):
        self.__pydb.add_symbol_in_watchlist([('SBIN',), ('ONGC',)])
        symbols = self.__pydb.get_stock_symobls_to_fetch_quotes()
        self.assertEqual((['SBIN', 'ONGC'], []), symbols)

    def test_fetch_stock_symbols_for_watchlist_and_position(self):
        self.__pydb.add_symbol_in_watchlist([('SAIL',), ('ONGC',), ('SBIN',)])
        position = ('SBIN', 100, 100)
        self.__pydb.add_position(position)
        symbols = self.__pydb.get_stock_symobls_to_fetch_quotes()
        self.assertEqual((['SAIL', 'ONGC', 'SBIN'], ['SBIN']), symbols)

    def test_add_position(self):
        add_position = ('SBIN', 100, 100)
        self.__pydb.add_position(add_position)
        position = self.__pydb.get_positions()
        self.assertEqual({'SBIN': {'symbol': 'SBIN', 'qty': 100, 'buy_price': 100}}, position)

    def test_add_more_position(self):
        add_position = ('SBIN', 100, 100)
        self.__pydb.add_position(add_position)
        add_position = ('SBIN', 100, 200)
        self.__pydb.add_position(add_position)
        position = self.__pydb.get_positions()
        self.assertEqual({'SBIN': {'buy_price': 150, 'qty': 200, 'symbol': 'SBIN'}}, position)

    def test_update_position(self):
        add_position = ('SBIN', 100, 100)
        self.__pydb.add_position(add_position)
        self.__pydb.update_position(('SBIN', 50, 200))
        position = self.__pydb.get_positions()
        self.assertEqual({'SBIN': {'buy_price': 100, 'qty': 50, 'symbol': 'SBIN'}}, position)

    def test_remove_position(self):
        add_position = ('SBIN', 100, 100)
        self.__pydb.add_position(add_position)
        self.__pydb.update_position(('SBIN', 100, 200))
        position = self.__pydb.get_positions()
        self.assertEqual({}, position)