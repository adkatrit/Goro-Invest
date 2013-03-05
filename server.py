import tornado.ioloop
import tornado.web

from goro import FinanceStream, YahooStream
import settings


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pass


def setup():
    fnames = [settings._sharpe, settings._range]
    fs = FinanceStream()
    stock_data, range_data = [fs.load_data(fn) for fn in fnames]

    for sd, rd in zip(stock_data, range_data):
        ys = YahooStream(sd[0], sd[1])
        for x in ys.open_conn():
            print x

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
