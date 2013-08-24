import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class ShoppintCart(object):
    pass

class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class CartHandler(tornado.web.RequestHandler):
    def post(self):
        pass

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        pass

class Application(tornado.web.Application):
    def __init__(self):
        self.shoppintCart = ShoppintCart()
        
        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler),
        ]

        setting = {
            'template_path': 'templates',
            'static_path': 'static',
        }
        tornado.web.Application.__init__(self, handlers, **setting)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

