from prompt_toolkit import HTML
from prompt_toolkit.layout import HSplit, Window, FormattedTextControl, WindowAlign, VSplit, FloatContainer, Float, \
    CompletionsMenu, Layout
from prompt_toolkit.widgets import Frame

from pyticker.view.bottom_input_instructions_view import BottomInputInstructionsView
from pyticker.view.positions_view import PositionsView
from pyticker.view.pyticker_styles import PyTickerStyles
from pyticker.view.watchlist_view import WatchListView


class PyTickerLayout(object):
    def __init__(self):
        self.__watchlist = WatchListView()
        self.__positions = PositionsView()
        self.__bottom = BottomInputInstructionsView()

    def _get_main_title_layout(self):
        return Frame(Window(FormattedTextControl(HTML("<u>PyTicker</u>")), height=1, align=WindowAlign.CENTER),
                     style=PyTickerStyles.DARK_GREY_BACKGROUND_BLACK_TEXT)

    def _get_columns_layout(self):
        return VSplit(
            [
                HSplit([
                    self.__watchlist.get_watchlist_title_view(),
                    self.__watchlist.get_watchlist_column_view()
                ]),
                HSplit([
                    self.__positions.get_positions_title_view(),
                    self.__positions.get_positions_column_view()
                ]),

            ],
            height=2, padding=1, padding_style="bg:#e5e7e9",
        )

    def _get_main_content_layout(self):
        return VSplit([
            self.__watchlist.get_watchlist_stocks_view(),
            self.__positions.get_positions_stocks_view()
        ],
            padding=1,
            padding_char=".",
        )

    def get_layout(self) -> Layout:
        root_container = HSplit([
            self._get_main_title_layout(),
            self._get_columns_layout(),
            self._get_main_content_layout(),
            Window(width=2, height=1, char="."),
            self.__bottom.get_input_instructions_view()
        ])
        root_container = FloatContainer(
            root_container,
            floats=[
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=16, scroll_offset=1),
                ),
            ],
        )
        return Layout(container=root_container)
