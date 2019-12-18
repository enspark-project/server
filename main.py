from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


@socketio.on('message')
def msg(msg):
    print('msg ', msg)


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
