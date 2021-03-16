import unittest

from pyticker.get_stock_quote import YahooHttpClient


class GetStockQuote(unittest.TestCase):
    def setUp(self) -> None:
        self._yahoo_client = YahooHttpClient()

    def test_fetch_stock_quotes(self):
        symbols = 'SBIN.NS,ONGC.NS'
        quotes = self._yahoo_client.get_watchlist_text(symbols)

        self.assertEqual(len(quotes), 2)
        style, quote_text = quotes[0]
        self.assertIsNotNone(style)
        self.assertIsNotNone(quote_text)

    def test_fetch_stock_quotes_when_one_of_the_symbols_is_wrong(self):
        symbols = 'SBIN.NS,invalid'
        quotes = self._yahoo_client.get_watchlist_text(symbols)

        self.assertEqual(len(quotes), 1)
        style, quote_text = quotes[0]
        self.assertIsNotNone(style)
        self.assertIsNotNone(quote_text)