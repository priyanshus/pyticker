import unittest

from pyticker.util import PyTickerDBOperations


class PyTickerDBOperationsTest(unittest.TestCase):
    def setUp(self) -> None:
        self._pyfolio_db = PyTickerDBOperations()

    def test_add_stocks_to_watchlist(self):
        pass