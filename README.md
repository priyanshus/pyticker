[![Python package](https://github.com/priyanshus/pyticker/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/priyanshus/pyticker/actions/workflows/test.yml)
# pyticker
Terminal App for Stock Watchlisting and Position Tracking. Uses Yahoo Finance to fetch the real time stock quotes.

![screenrecord](https://user-images.githubusercontent.com/6668813/111755990-b9119380-88bf-11eb-80b7-2870f8ecdf96.gif)

### Features
✨ Real time stock quotes. 

✨ Live position tracking.

✨ Fetches latest quotes every second.

✨ Stocks/Positions can be added/removed from CLI.

### How to Use
```sh
pip install pyticker
pyticker
```
### To add/remove stocks
At the bottom of the app, there is an istruction text area. It autosuggests available commands to operate the Pyticker. For example, to add the stock in watchlist an instruction like `add_to_watchlist SBIN.NS ONGC.NS` can be issued.

**Supported Instructions**


| Instruction | Example | Remarks |
| ------ | ------ | ------ |
| add_to_watchlist | add_to_watchlist <stock-symbol-1> <stock-symbol-2> | Stock Symbols separate by white space |
| remove_from_watchlist | remove_from_watchlist <stock-symbol | remove_from_watchlist SBIN.NS |
| add_new_position | add_new_position <stock-symbol> <qty> <entry-price> | example: add_new_position SBIN.NS 100 200 |
| remove_from_position | remove_from_position <stock-symbol> | remove_from_position SBIN.NS |
  
### Credits
- [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)
- Yahoo Finance
- [Inspired by Ticker](https://github.com/achannarasappa/ticker)
  
### License
MIT
