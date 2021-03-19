from dataclasses import dataclass

from dataclasses_json import dataclass_json, LetterCase
from typing import List


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class DataFormat:
    raw: int
    fmt: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Result:
    symbol: str
    short_name: str
    regular_market_change: DataFormat
    regular_market_price: DataFormat
    regular_market_previous_close: DataFormat
    regular_market_open: DataFormat
    regular_market_day_low: DataFormat
    regular_market_day_high: DataFormat

    def get_symbol(self) -> str:
        return self.symbol.replace('.NS','') if self.symbol.endswith('.NS') else self.symbol


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class QuoteResponse:
    result: List[Result]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class YahooQuoteResponse:
    quote_response: QuoteResponse


def get_int_value(data: DataFormat) -> int:
    return data.raw


def get_str_value(data: DataFormat) -> str:
    return data.fmt
