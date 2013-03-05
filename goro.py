import urllib2
import math
import operator
import pickle
import contextlib

from numpy import mean, std, array

import settings


class FinanceStream(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.prefix = "YTD"
        self.ytd_url = settings._YAHOO_YTD

    def get_sharpe_ratio(self, prices):
        return math.sqrt(250) * (mean(array(prices)) / std(array(prices)))

    def load_data(self, fname):
        return pickle.load(open("%s%s" % (self.prefix, fname), "rb"))


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
                yield(x.read())


def run():
    fnames = ["sharpe.p", "range.p"]
    fs = FinanceStream()
    stock_data, range_data = [fs.load_data(fn) for fn in fnames]

    for sd, rd in zip(stock_data, range_data):
        ys = YahooStream(sd[0], sd[1])
        for x in ys.open_conn():
            pass


if __name__ == "__main__":
    run()
