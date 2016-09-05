from tornado import websocket, web, ioloop
import tornado
import json
import requests
import boto3

cl = []

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_close(self):
        if self in cl:
            cl.remove(self)

class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        subject = self.get_argument("subject")
        message = self.get_argument("message")
        data = {"subject": subject, "message" : message}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @web.asynchronous
    def post(self, *args, **kwargs):
        data = tornado.escape.json_decode(self.request.body)
        headers = self.request.headers
        message_type = headers['x-amz-sns-message-type']

        if message_type == 'SubscriptionConfirmation':
            pass
        elif message_type == 'Notification':
            pass
        elif message_type == 'UnsubscribeConfirmation':
            pass
        else:
            pass
        self.set_status(200)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/sns', ApiHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    app.listen(8000)
    ioloop.IOLoop.instance().start()
