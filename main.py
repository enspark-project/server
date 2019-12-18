import datetime
import json

from bson import ObjectId
from flask import Flask
from flask.json import jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

from database import read_robots, create_new_robot


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)




app = Flask(__name__)
app.json_encoder = JSONEncoder
CORS(app)
socketio = SocketIO(app, logger=True, engineio_logger=True, async_handlers=True)


@socketio.on('message')
def msg(msg):
    print('msg ', msg)


@socketio.on('read_all_robots')
def read_all_robots_command(data):
    return JSONEncoder().encode(read_robots())


@socketio.on('create_new_robot')
def create_new_robot_command(robot):
    create_new_robot(robot['name'], robot['key'], robot['robot_type'], robot['description'], robot['tags'])


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
