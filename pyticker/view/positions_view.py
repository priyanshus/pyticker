from prompt_toolkit import HTML
from prompt_toolkit.layout import Window, FormattedTextControl, WindowAlign

from pyticker.core.util import ProjectConstants
from pyticker.view.pyticker_styles import PyTickerStyles

POSITION_STOCKS_TEXT = FormattedTextControl(style="bold")


class PositionsView(object):
    def __init__(self):
        self.__width = ProjectConstants.WIDTH
        self.__positions_title_view_text = '<u>Positions</u>'
        self.__watchlist_subtitle_view_text = f'{"Symbol".ljust(self.__width)}{"Qty".ljust(6)}{"Inv Price".ljust(self.__width)}' \
                                              f'{"Total Inv".ljust(self.__width)}{"Mkt Price".ljust(self.__width)}{"Curr Val".ljust(self.__width)}' \
                                              f'{"Profit/Loss".ljust(self.__width)}'

    def get_positions_title_view(self) -> Window:
        return Window(
            FormattedTextControl(HTML(self.__positions_title_view_text)),
            height=1,
            ignore_content_width=True,
            style=PyTickerStyles.GREY_BACKGROUND_BLACK_TEXT,
            align=WindowAlign.CENTER,
        )

    def get_positions_column_view(self) -> Window:
        return Window(
            content=FormattedTextControl(self.__watchlist_subtitle_view_text),
            ignore_content_width=True,
            style=PyTickerStyles.GREY_BACKGROUND_BLACK_TEXT,
            align=WindowAlign.LEFT,
        )

    def get_positions_stocks_view(self):
        return Window(content=POSITION_STOCKS_TEXT,
                      ignore_content_width=True,
                      align=WindowAlign.LEFT)
