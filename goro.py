import urllib2
import math
import operator
import pickle

from numpy import mean, std, array

from .goro_invest import settings

url = settings._YAHOO_YTD


class FinanceStream(object):
    def __init__(self, stock_data, range_data):
        self.stock_data = stock_data
        self.range_data = range_data
        self.prefix = "YTD"

    def get_sharpe_ratio(self, prices):
        return math.sqrt(250) * (mean(array(prices)) / std(array(prices)))

    def load_data(self, fname):
        return pickle.load(open("%s%s" % (self.prefix, fname), "rb"))


class StockSymbol(FinanceStream):
    def __init__(self, symbol, symbol_range):
        super(StockSymbol, self).__init__(symbol, symbol_range)
