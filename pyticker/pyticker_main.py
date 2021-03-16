import threading

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings

from pyticker.get_stock_quote import YahooHttpClient
from pyticker.util import PyTickerDBOperations, every
from pyticker.view.positions_view import PositionsView
from pyticker.view.pyticker_layout import PyTickerLayout
from pyticker.view.watchlist_view import WatchListView, WATCHLIST_STOCKS_TEXT


bindings = KeyBindings()


@bindings.add('c-c')
def _(event):
    event.app.exit()


class PyTicker(object):
    def __init__(self):
        self._application = None
        self._pyticker_layout = PyTickerLayout()
        self._watchlist_view = WatchListView()
        self._positions_view = PositionsView()
        self._yahoo_client = YahooHttpClient()
        self._pyticker_db = PyTickerDBOperations()

    def init_application(self):
        self._pyticker_db.init_db()
        layout = self._pyticker_layout.get_layout()
        self._application = Application(layout=layout, full_screen=True, key_bindings=bindings)

    def _invalidate(self):
        WATCHLIST_STOCKS_TEXT.text = self._yahoo_client.get_watchlist_text(self._pyticker_db.get_watchlist_symbols())
        self._application.invalidate()

    def run(self):
        watchlist_stock_symbols = self._pyticker_db.get_watchlist_symbols()
        WATCHLIST_STOCKS_TEXT.text = self._yahoo_client.get_watchlist_text(watchlist_stock_symbols)
        threading.Thread(target=lambda: every(1, self._invalidate), daemon=True).start()
        self._application.run()

def main():
    pyticker = PyTicker()
    pyticker.init_application()
    pyticker.run()

if __name__ == '__main__':
    main()
