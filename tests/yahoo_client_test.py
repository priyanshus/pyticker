import unittest
import os
import pathlib

from pyticker.core.pyticker_db_operations import PyTickerDBOperations
from pyticker.core.yahoo_client import YahooHttpClient


class GetStockQuote(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.__file = open(os.path.join(pathlib.Path().absolute(), 'test.db'), "w")
        self.__pydb = PyTickerDBOperations(os.path.join(pathlib.Path().absolute(), 'test.db'))
        self.__pydb.init_db()
        self.__pydb.add_position(('SBIN.NS', 100, 100))

    @classmethod
    def tearDownClass(self) -> None:
        pathlib.Path(os.path.join(pathlib.Path().absolute(), 'test.db')).unlink()

    def test_fetch_stock_quotes(self):
        yahoo_client = YahooHttpClient(['SBIN.NS'], ['SBIN.NS'], self.__pydb)
        quotes = yahoo_client.get_stock_quotes()
        self.assertIsNotNone(quotes)
        self.assertEqual(len(quotes), 2)

    def test_fetch_stock_quotes_when_one_of_the_symbols_is_wrong(self):
        self.__pydb.add_position(('SBINX', 100, 100))
        yahoo_client = YahooHttpClient(['SBIN.NS'], ['XYZ'], self.__pydb)
        quotes = yahoo_client.get_stock_quotes()
        self.assertIsNotNone(quotes)
        self.assertEqual(2, len(quotes))
        self.assertEqual([], quotes[1])
