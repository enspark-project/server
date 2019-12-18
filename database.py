from pymongo import MongoClient

client = MongoClient('localhost')

database = client.enspark


def create_new_robot(name, key, robot_type, description, tags):
    database.robots.insert_one({
        'name': name,
        'key': key,
        'robot_type': robot_type,
        'description': description,
        'tags': tags
    })


def update_robot_data(id, name, key, description, tags):
    database.robots.update_one({'_id': id}, {
        'name': name,
        'key': key,
        'description': description,
        'tags': tags
    })


def delete_robot(id):
    database.robots.delete_one({'_id': id})


def read_robots():
    return list(database.robots.find({}))
