from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.widgets import TextArea

from pyticker.core.pyticker_db_operations import PyTickerDBOperations
from pyticker.view.pyticker_styles import PyTickerStyles


class BottomInputInstructionsView(object):
    def __init__(self):
        self.__completer = WordCompleter([
            'add_to_watchlist',
            'remove_from_watchlist',
        'add_new_position',
        'remove_from_position'], ignore_case=True)
        self.__pyticker_db = PyTickerDBOperations()

    def get_input_instructions_view(self):
        return TextArea(height=1,
                        prompt=">>> ",
                        style=PyTickerStyles.INPUT_FIELD,
                        complete_while_typing=True,
                        multiline=False,
                        wrap_lines=False,
                        completer=self.__completer,
                        accept_handler=self._instruction_processor)

    def _instruction_processor(self, buff):
        """
        Process space separated stock symbols
        :param buff:
        :return:
        """
        symbols_to_process = [(symbol,) for symbol in buff.text.split()[1:]]

        if buff.text.__contains__('add_to_watchlist'):
            self.__pyticker_db.add_symbol_in_watchlist(symbols_to_process)
        elif buff.text.__contains__('remove_from_watchlist'):
            self.__pyticker_db.delete_symbol_in_watchlist(symbols_to_process)
        elif buff.text.__contains__('add_new_position'):
            position_details = tuple(buff.text.split()[1:])
            self.__pyticker_db.add_position(position_details)
        elif buff.text.__contains__('remove_from_position'):
            position_details = tuple(buff.text.split()[1:])
            self.__pyticker_db.update_position(position_details)
