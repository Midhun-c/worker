from flask_login import UserMixin
from bson.objectid import ObjectId
from app import mongo, bcrypt

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        mongo.db.users.insert_one({
            'username': self.username,
            'password': bcrypt.generate_password_hash(self.password).decode('utf-8')
        })

    @staticmethod
    def get_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(username=user_data['username'], password=user_data['password'])
        return None

    def get_id(self):
        return self.username  # or another unique identifier like user_data['_id']

class Worker:
    def __init__(self, name, location, photo, employment_history, user_id):
        self.name = name
        self.location = location
        self.photo = photo
        self.employment_history = employment_history
        self.user_id = user_id

    def save_to_db(self):
        mongo.db.workers.insert_one({
            'name': self.name,
            'location': self.location,
            'photo': self.photo,
            'employment_history': self.employment_history,
            'user_id': self.user_id
        })

    @staticmethod
    def get_all_workers_by_user(user_id):
        return list(mongo.db.workers.find({'user_id': user_id}))

    @staticmethod
    def get_worker_by_id(worker_id):
        return mongo.db.workers.find_one({'_id': ObjectId(worker_id)})

    @staticmethod
    def update_worker(worker_id, updated_data):
        mongo.db.workers.update_one({'_id': ObjectId(worker_id)}, {'$set': updated_data})

    @staticmethod
    def delete_worker(worker_id):
        mongo.db.workers.delete_one({'_id': ObjectId(worker_id)})
