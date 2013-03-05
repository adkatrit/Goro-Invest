import tornado.ioloop
import tornado.web

from goro import FinanceStream, YahooStream
import settings


def render_stock_data():
    stock_attr = {}
    fs = FinanceStream()
    fnames = [settings._sharpe, settings._range]
    stock_data, range_data = [fs.load_data(fn) for fn in fnames]

    for sd, rd in zip(stock_data, range_data):
            ys = YahooStream(sd[0], sd[1])
            for x in ys.open_conn():
                stock_attr[ys.symbol] = x

    return stock_attr


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Dont run -- throwing HTTP error
        stock_attr = render_stock_data()
        self.write(stock_attr)


application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
