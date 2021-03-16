from prompt_toolkit import HTML
from prompt_toolkit.layout import FormattedTextControl, Window, WindowAlign

from pyticker.util import ProjectConstants
from pyticker.view.pyticker_styles import PyTickerStyles

WATCHLIST_STOCKS_TEXT = FormattedTextControl(style="bold")


class WatchListView(object):
    def __init__(self):
        self._width = ProjectConstants.WIDTH
        self._watchlist_title_view_text = f"<u>Watchlist</u>"
        self._watchlist_subtitle_view_text = f'{"Symbol".ljust(self._width)}{"Pr Close".ljust(self._width)}{"Open".ljust(self._width)}' \
                                             f'{"D Low".ljust(self._width)}{"D High".ljust(self._width)}{"Mkt Price".ljust(self._width)}' \
                                             f'{"Change".ljust(self._width)}'

    def get_watchlist_title_view(self) -> Window:
        return Window(
            FormattedTextControl(HTML(self._watchlist_title_view_text)),
            height=1,
            ignore_content_width=True,
            style=PyTickerStyles.GREY_BACKGROUND_BLACK_TEXT,
            align=WindowAlign.CENTER,
        )

    def get_watchlist_subtitle_view(self) -> Window:
        return Window(
            content=FormattedTextControl(self._watchlist_subtitle_view_text),
            ignore_content_width=True,
            style=PyTickerStyles.GREY_BACKGROUND_BLACK_TEXT,
            align=WindowAlign.LEFT,
        )

    def get_watchlist_stocks_view(self):
        return Window(content=WATCHLIST_STOCKS_TEXT,
                      ignore_content_width=True,
                      align=WindowAlign.LEFT)
