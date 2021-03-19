from prompt_toolkit import HTML
from prompt_toolkit.layout import FormattedTextControl, Window, WindowAlign

from pyticker.core.util import ProjectConstants
from pyticker.view.pyticker_styles import PyTickerStyles

WATCHLIST_STOCKS_TEXT = FormattedTextControl(style="bold")


class WatchListView(object):
    def __init__(self):
        self.__width = ProjectConstants.WIDTH
        self.__watchlist_title_view_text = '<u>Watchlist</u>'
        self.__watchlist_subtitle_view_text = f'{"Symbol".ljust(self.__width)}{"Pr Close".ljust(self.__width)}{"Open".ljust(self.__width)}' \
                                              f'{"D Low".ljust(self.__width)}{"D High".ljust(self.__width)}{"Mkt Price".ljust(self.__width)}' \
                                              f'{"Change".ljust(self.__width)}'

    def get_watchlist_title_view(self) -> Window:
        return Window(
            FormattedTextControl(HTML(self.__watchlist_title_view_text)),
            height=1,
            ignore_content_width=True,
            style=PyTickerStyles.GREY_BACKGROUND_BLACK_TEXT,
            align=WindowAlign.CENTER,
        )

    def get_watchlist_column_view(self) -> Window:
        return Window(
            content=FormattedTextControl(self.__watchlist_subtitle_view_text),
            ignore_content_width=True,
            style=PyTickerStyles.GREY_BACKGROUND_BLACK_TEXT,
            align=WindowAlign.LEFT,
        )

    def get_watchlist_stocks_view(self):
        return Window(content=WATCHLIST_STOCKS_TEXT,
                      ignore_content_width=True,
                      align=WindowAlign.LEFT)
