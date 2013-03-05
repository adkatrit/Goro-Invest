import urllib2
import math
import operator
import pickle
import contextlib
import logging

from numpy import mean, std, array

import settings

logging.basicConfig(filename="error.log", level=logging.DEBUG)


class FinanceStream(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.prefix = "YTD"
        self.ytd_url = settings._YAHOO_YTD

    def get_sharpe_ratio(self, prices):
        return math.sqrt(250) * (mean(array(prices)) / std(array(prices)))

    def load_data(self, fname):
        return pickle.load(open("%s" % (fname), "rb"))


class StockSymbol(FinanceStream):
    def __init__(self, symbol, symbol_range, *args, **kwargs):
        super(StockSymbol, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.symbol_range = symbol_range


class YahooStream(StockSymbol):
    def __init__(self, *args, **kwargs):
        super(YahooStream, self).__init__(*args, **kwargs)

    def open_conn(self):
        if self.symbol:
            with contextlib.closing(urllib2.urlopen("%s%s" %
                                   (self.ytd_url, self.symbol))) as x:
                try:
                    yield(x.read())
                except urllib2.HTTPError:
                    logging.debug("Throwing HTTPError")
