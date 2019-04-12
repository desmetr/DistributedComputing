import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime

class MainHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        self.connections.add(self)

    def on_message(self, message):
        [client.write_message(message) for client in self.connections]

    def on_close(self):
        self.connections.remove(self)

    def check_origin(self, origin):
        return origin=="http://localhost:5000"
    
def make_app():
    return tornado.web.Application([
        (r"/websocket", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()