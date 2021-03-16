from prompt_toolkit import HTML
from prompt_toolkit.layout import Window, FormattedTextControl, WindowAlign

from pyticker.view.pyticker_styles import PyTickerStyles

POSITION_STOCKS_TEXT = FormattedTextControl(style="bold")


class PositionsView(object):
    def __init__(self):
        self._positions_title_view_text = f"<u>Positions</u>"

    def get_positions_title_view(self) -> Window:
        return Window(
            FormattedTextControl(HTML(self._positions_title_view_text)),
            height=1,
            ignore_content_width=True,
            style=PyTickerStyles.GREY_BACKGROUND_BLACK_TEXT,
            align=WindowAlign.CENTER,
        )

    def get_positions_stocks_view(self):
        return Window(content=POSITION_STOCKS_TEXT,
                      ignore_content_width=True,
                      align=WindowAlign.LEFT)
