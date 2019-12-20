import datetime
import json

from bson import ObjectId
from flask import Flask, request
from flask.json import jsonify
from flask_cors import CORS
from flask_socketio import SocketIO

from database import read_robots, create_new_robot, delete_robot, update_robot_data, push_gyro_data


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


clients = []
robots = []

app = Flask(__name__)
app.json_encoder = JSONEncoder
CORS(app)
socketio = SocketIO(app, logger=True, engineio_logger=True, async_handlers=True)


@socketio.on('robot_register')
def register(id, key):
    robots[id] = request.namespace


@socketio.on('move')
def move(id, type, direction, delta):
    robots[id].emit('robot_move', type, direction, delta)


@socketio.on('push_gyro_data')
def push_data(gyro_record):
    push_gyro_data(gyro_record['robot_id'], gyro_record['x'], gyro_record['y'], gyro_record['z'], gyro_record['a'],
                   gyro_record['b'], gyro_record['c'])


@socketio.on('connect')
def connected():
    clients.append(request.namespace)


@socketio.on('disconnect')
def disconnect():
    clients.remove(request.namespace)


@socketio.on('read_all_robots')
def read_all_robots_command(data):
    return JSONEncoder().encode(read_robots())


@socketio.on('create_new_robot')
def create_new_robot_command(robot):
    create_new_robot(robot['name'], robot['key'], robot['robot_type'], robot['description'], robot['tags'])


@socketio.on('delete_robot')
def delete_robot_command(id):
    delete_robot(id)


@socketio.on('update_robot')
def update_robot_command(robot):
    update_robot_data(robot['id'], robot['name'], robot['key'], robot['description'], robot['tags'])


if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
