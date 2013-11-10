import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class ShoppingCart(object):
    total_inventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def add_to_cart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notify_callbacks()

    def remove_from_cart(self, session):
        if session not in self.carts:
            return 

        del(self.carts[session])
        self.notify_callbacks()

    def notify_callbacks(self):
        for callback in self.callbacks:
            callback(self.get_inventory_count())

        self.callbacks[:] = []
        
    def get_inventory_count(self):
        return self.total_inventory - len(self.carts)
    
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.shopping_cart.get_inventory_count()
        self.render('index.html', session=session, count=count)

class CartHandler(tornado.web.RequestHandler):
    def post(self):
        session = self.get_argument('session')
        action = self.get_argument('action')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.shopping_cart.add_to_cart(session)
        elif action == 'remove':
            self.application.shopping_cart.remove_from_cart(session)
        else:
            self.set_status(400)

class StatusHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.application.shopping_cart.register(self.async_callback(self.on_message))

    def on_message(self, count):
        self.write('{"inventory_count":"%d"}' % count)
        self.finish()

class Application(tornado.web.Application):
    def __init__(self):
        self.shopping_cart = ShoppingCart()
        
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

