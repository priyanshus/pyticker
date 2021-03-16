from typing import List
import requests

from pyticker.util import ProjectConstants
from pyticker.yahoo_response_model import YahooQuoteResponse, get_str_value, Result


def _get_style_for_watchlist(change_price: str):
    return "#d12d0d " if change_price.startswith('-') else "#0dba3a"


class YahooHttpClient(object):
    def __init__(self):
        self._width = ProjectConstants.WIDTH
        self._yahoo_url = "https://query2.finance.yahoo.com/v7/finance/quote?formatted=true&symbols={}"

    def _fetch_stock_quote(self, symbols) -> str:
        if symbols:
            response = requests.get(self._yahoo_url.format(symbols))
            if response.status_code == 200:
                return response.text
            else:
                print('Something wrong with yahoo finance..')
        return None

    def get_watchlist_text(self, stock_symbols) -> List[tuple]:
        watchlist_text_list = []
        quotes = self._fetch_stock_quote(stock_symbols)
        if quotes:
            results = YahooQuoteResponse.from_json(quotes).quote_response.result
            for result in results:
                watchlist_text_list.append(self._format_watchlist_text(result))

            return watchlist_text_list

    def _format_watchlist_text(self, result: Result) -> tuple:
        symbol = result.get_symbol().ljust(self._width)
        market_price = get_str_value(result.regular_market_price).ljust(self._width)
        regular_market_open = get_str_value(result.regular_market_open).ljust(self._width)
        previous_day_close = get_str_value(result.regular_market_previous_close).ljust(self._width)
        day_low = get_str_value(result.regular_market_day_low).ljust(self._width)
        day_high = get_str_value(result.regular_market_day_high).ljust(self._width)
        market_change = get_str_value(result.regular_market_change)

        watchlist_style = _get_style_for_watchlist(market_change)
        watchlist_text = symbol + previous_day_close + regular_market_open + day_low + day_high + market_price + market_change + '\n'
        return watchlist_style, watchlist_text
