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
        subject = self.get_argument("id")
        message = self.get_argument("value")
        data = {"id": subject, "value" : message}
        data = json.dumps(data)
        for c in cl:
            c.write_message(data)

    @web.asynchronous
    def post(self, *args, **kwargs):
        data = tornado.escape.json_decode(self.request.body)
        headers = self.request.headers
        message_type = headers['x-amz-sns-message-type']

        if message_type == 'SubscriptionConfirmation':
            print('Receive subscription confirmation from {}'.format(h['x-amz-sns-topic-arn']))
            pprint(data)
            print('Sending confirmation...')
            res = requests.get(data['SubscribeURL'])
            print('Confirmation: Done, status: {}'.format(res.status_code))

        elif message_type == 'Notification':
            print('Receive notification')
            print('TopicArn: {}'.format(data['TopicArn']))
            print('Subject: {}'.format(data['Subject']))
            print('Message: {}'.format(data['Message']))
            print('Timestamp: {}'.format(data['Timestamp']))
            # push the message to clients
            msg = {
                'subject': data['Subject'],
                'message': data['Message'],
                'timestamp': data['Timestamp']
            }
            msg = json.dumps(msg)
            for c in cl:
                c.write_message(msg)

        elif message_type == 'UnsubscribeConfirmation':
            print('Receive UnsubscribeConfirmation')

        else:
            print('Don\'t understand this header: {}'.format(message_type))

        self.set_status(200)
        self.finish()

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', SocketHandler),
    (r'/sns', ApiHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])

if __name__ == '__main__':
    address = '0.0.0.0'
    port = 8000
    app.listen(port, address)
    ioloop.IOLoop.instance().start()
