from flask_app import app, DB
from flask_app.config.mysqlconnection import connectToMySQL

class Key_Stats:
    def __init__(self, data):
        self.id = data['id'],
        self.str = data['str'],
        self.agy = data['agy'],
        self.sta = data['sta'],
        self.int = data['int'],
        self.cha = data['cha'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

        @classmethod
        def save(cls, data):