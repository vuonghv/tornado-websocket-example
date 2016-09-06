# Amazone SNS using Tornado WebSocket

Display messages (published from AWS SNS) by using Tornado WebSocket

## Preconfiguration
Setting your Amazon credentials for Boto 3. You ONLY need this settings if you
want to publish messages to AWS SNS Topic through bellow REST API.
Make sure your key have permission to publish message.

1. Create the credential file, its default location is at `$HOME/.aws/credentials`:

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```
2. Set a default region, its location is at `$HOME/.aws/config`:

```
[default]
region=us-east-2
```

## Installation

1. `git clone https://github.com/vuonghv/sns-tornado-websocket.git`

2. `cd sns-tornado-websocket`

3. Edit `index.html`: `var socket_url = 'ws://localhost:8000/ws` <- change to your url/localhost

4. (Optional) If you want to publish message to AWS SNS, then config `TOPIC_ARN` in file `app.py`

5. `pip install -r requirements.txt`

6. `python app.py`

7. Visit: `http://localhost:8000/`
(This is demo page -> http://mangxa.framgia.vn/)

8. Make some below GET requests to see the magics. :)


## REST API examples

* **Publish message to Amazon SNS**

GET /publish: `http://localhost:8000/publish?subject=who_are_you&message=do_you_know_whoami`

* **Test Tornado WebSocket**

GET /sns: `http://localhost:8000/sns?subject=who_are_you&message=do_you_know_whoami`


## Thanks

* [hiroakis](https://github.com/hiroakis/tornado-websocket-example) for a greate example of Tornado WebSocket.

## License

MIT
