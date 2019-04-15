import tornado.ioloop
import tornado.web
import tornado.websocket

class MainHandler(tornado.websocket.WebSocketHandler):
    connections = {}

    def open(self):
        print(self.request.uri[10:])
        if not self.request.uri[10:] in self.connections:
            self.connections[self.request.uri[10:]]=set()
        self.connections[self.request.uri[10:]].add(self)

    def on_message(self, message):
        print("message from: " + self.request.uri)
        [client.write_message(message) for client in self.connections[self.request.uri[10:]]]
        [print(client) for client in self.connections[self.request.uri[10:]]]

    def on_close(self):
        print("closing: " + self.request.uri)
        if len(self.connections[self.request.uri[10:]])==1:
            del self.connections[self.request.uri[10:]]
        else:
            self.connections[self.request.uri[10:]].remove(self)

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
