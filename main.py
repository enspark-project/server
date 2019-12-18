from flask import Flask
from flask_socketio import SocketIO

from flask_cors import CORS

from database import read_robots

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, logger=True, engineio_logger=True, async_handlers=True)


@socketio.on('message')
def msg(msg):
    print('msg ', msg)


@socketio.on('read_all_robots')
def read_all_robots_command(data):
    return read_robots()


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
