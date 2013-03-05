import os

_YAHOO_BASE = "http://ichart.finance.yahoo.com/table.csv?a=00&b=1&c=2011&d=11&e=31&f=2011&g=d&ignore=.csv&s="
_YAHOO_YTD = "http://ichart.finance.yahoo.com/table.csv?a=10&b=8&c=2011&d=10&e=8&f=2012&g=d&ignore=.csv&s="

data_path = lambda x: os.path.abspath(os.path.join(os.path.dirname(__file__), x))
_sharpe = data_path("data/sharpe.p")
_range = data_path("data/range.p")
_NASDAQ = data_path("nasdaqlisted.txt")
