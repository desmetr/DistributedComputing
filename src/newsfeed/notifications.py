import tornado.ioloop
import tornado.web
import tornado.websocket
import json

class MainHandler(tornado.websocket.WebSocketHandler):
    connections = {}
    def open(self):
        print(self.request.uri)
        print(self.request.uri[15:])
        if self.request.uri[15:] != "sending":
            self.connections[self.request.uri[15:]] = self
        print(self.connections)
        print("---")

    def on_message(self, message):
        message = message.replace("&#34;","\"")
        message = message.replace("&#39;","'")
        print("message: "+message+", from: " + self.request.uri)
        messageDict = json.loads(message)

        for friend in messageDict["friends"]:
            print("looking at friend: " + str(friend))
            for client in self.connections:
                print("looking at client: " + str(client))
                if friend == client:
                    print("sending to: " + str(client))
                    self.connections[client].write_message(messageDict["postText"])

    def on_close(self):
        print("closing: " + self.request.uri)
        if self.request.uri[15:] != "sending":
            del self.connections[self.request.uri[15:]]
        print(self.connections)

    def check_origin(self, origin):
        return True
    
def make_app():
    return tornado.web.Application([
        (r"/notifications/[a-zA-Z0-9]*", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()