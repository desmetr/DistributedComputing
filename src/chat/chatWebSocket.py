import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime

class MainHandler(tornado.websocket.WebSocketHandler):
    connections = set()

    def open(self):
        print(self.request.uri)
        self.connections.add(self)

    def on_message(self, message):
        [client.write_message(message) for client in self.connections]

    def on_close(self):
        self.connections.remove(self)

    def check_origin(self, origin):
        return True
    
def make_app():
    return tornado.web.Application([
        (r"/websocket/[a-zA-Z0-9]*", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
