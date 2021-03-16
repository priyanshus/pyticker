from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.widgets import TextArea

from pyticker.util import PyTickerDBOperations
from pyticker.view.pyticker_styles import PyTickerStyles


class BottomInputInstructionsView(object):
    def __init__(self):
        self._completer = WordCompleter([
            'add_to_watchlist', 'remove_from_watchlist'], ignore_case=True)
        self._pyticker_db = PyTickerDBOperations()

    def get_input_instructions_view(self):
        return TextArea(height=1,
                        prompt=">>> ",
                        style=PyTickerStyles.INPUT_FIELD,
                        complete_while_typing=True,
                        multiline=False,
                        wrap_lines=False,
                        completer=self._completer,
                        accept_handler=self._instruction_processor)

    def _instruction_processor(self, buff):
        symbols_to_process = [(symbol,) for symbol in buff.text.split()[1:]]

        if buff.text.__contains__('add_to_watchlist'):
            self._pyticker_db.add_symbol_in_watchlist(symbols_to_process)
        elif buff.text.__contains__('remove_from_watchlist'):
            self._pyticker_db.delete_symbol_in_watchlist(symbols_to_process)
