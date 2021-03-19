from typing import List
import requests

from concurrent.futures import ThreadPoolExecutor
from pyticker.core.pyticker_db_operations import PyTickerDBOperations
from pyticker.core.util import ProjectConstants
from pyticker.core.yahoo_response_model import YahooQuoteResponse, get_str_value, Result, get_int_value


def _get_style_for_watchlist(change_price: str):
    return "#d12d0d " if change_price.startswith('-') else "#0dba3a"


class YahooHttpClient(object):
    """
    Yahoo http client
    :constructor: list_of_watchlist_symbols, list_of_position_symbols
    """

    def __init__(self, watchlist_symbols, position_symbols):
        self.__width = ProjectConstants.WIDTH
        self.__watchlist_symbols = watchlist_symbols
        self.__position_symbols = position_symbols
        self.__pyticker_db = PyTickerDBOperations()
        self.__stock_quotes = list()
        self.__yahoo_url = "https://query2.finance.yahoo.com/v7/finance/quote?formatted=true&symbols={}"

    def _talk_to_yahoo(self, symbol):
        response = requests.get(self.__yahoo_url.format(symbol))
        if response.status_code == 200:
            return response.text
        else:
            return None

    def _fetch_stock_quote(self) -> List[Result]:
        symbols = set(self.__watchlist_symbols + self.__position_symbols)
        responses = []
        results = []
        if symbols:
            with ThreadPoolExecutor(max_workers=10) as executor:
                responses = executor.map(self._talk_to_yahoo, symbols)

        if responses:
            for response in responses:
                results.append(YahooQuoteResponse.from_json(response).quote_response.result[0])
        return results

    def get_stock_quotes(self) -> tuple:
        """
        Get stock quotes
        :return: list_of_watchlist_formatted_text, list_of_positions_formatted_text
        """
        watchlist_text_list = []
        position_text_list = []
        results = self._fetch_stock_quote()
        if not results:
            return '', ''

        positions_in_hand = self.__pyticker_db.get_positions()
        for result in results:
            if result.symbol in self.__watchlist_symbols:
                watchlist_text_list.append(self._format_watchlist_text(result))
            if result.symbol in self.__position_symbols:
                position_text_list.append(self._format_position_text(positions_in_hand, result))

        return watchlist_text_list, position_text_list

    def _format_watchlist_text(self, result: Result) -> tuple:
        symbol = result.get_symbol().ljust(self.__width)
        market_price = get_str_value(result.regular_market_price).ljust(self.__width)
        regular_market_open = get_str_value(result.regular_market_open).ljust(self.__width)
        previous_day_close = get_str_value(result.regular_market_previous_close).ljust(self.__width)
        day_low = get_str_value(result.regular_market_day_low).ljust(self.__width)
        day_high = get_str_value(result.regular_market_day_high).ljust(self.__width)
        market_change = get_str_value(result.regular_market_change)

        watchlist_style = _get_style_for_watchlist(market_change)
        watchlist_text = symbol + previous_day_close + regular_market_open + day_low + day_high + market_price + market_change + '\n'
        return watchlist_style, watchlist_text

    def _format_position_text(self, position_in_hand: dict, result: Result) -> tuple:
        buy_price = position_in_hand[result.symbol]['buy_price']
        qty = position_in_hand[result.symbol]['qty']
        total_investment_int = round((qty * buy_price), 2)
        current_valuation_int = round(qty * get_int_value(result.regular_market_price), 2)
        symbol = result.get_symbol().ljust(self.__width)
        market_price = get_str_value(result.regular_market_price).ljust(self.__width)
        total_investment = str(total_investment_int).ljust(self.__width)
        current_valuation = str(current_valuation_int).ljust(self.__width)
        profit_or_loss = str(current_valuation_int - total_investment_int).ljust(self.__width)
        position_style = _get_style_for_watchlist(profit_or_loss)
        qty_str = str(qty).ljust(6)
        buy_price_str = str(buy_price).ljust(self.__width)
        position_text = symbol + qty_str + buy_price_str + total_investment + market_price + current_valuation + profit_or_loss + '\n'

        return position_style, position_text
