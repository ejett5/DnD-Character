from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DB
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA]+$')


#CREATE USER
class User:

    def __init__(self, data):
        self.id =           data["id"]
        self.first_name =   data["first_name"]
        self.last_name =    data["last_name"]
        self.email =        data["email"]
        self.password =     data["password"]
        self.created_at =   data["created_at"]
        self.updated_at =   data["updated_at"]
        self.trees =      []



#making the user
    @classmethod
    def create_user(cls, user_data):
        if not cls.validate_user_data(user_data):
            return False
        user_data = user_data.copy()
        user_data['password'] = bcrypt.generate_password_hash(user_data['password'])

        query = '''
        INSERT INTO user (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;'''

        user_id =  connectToMySQL(DB).query_db(query, user_data)
        session['user_id'] = user_id
        session['user_name'] = user_id
        session['user_name'] = f"{user_data['first_name']}"

        return user_data



# READ USER 
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email }
        query = '''
        SELECT *
        FROM user
        WHERE email = %(email)s
        ;'''
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return (cls(result[0]))
        return False

    @classmethod
    def get_user_by_id(cls, id):
        data = {'id' : id }
        query = '''
        SELECT *
        FROM user
        WHERE email = %(id)s
        ;'''
        result = connectToMySQL(DB).query_db(query, data)
        if result:
            return (cls(result[0]))
        return False



#accept user login credentials
    @classmethod
    def login(cls, data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash('Your login information was incorrect.')
        return False




#VALIDATION  
    @classmethod
    def validate_user_data(cls, data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            is_valid = False
            flash('Your first name must contain at least two characters')

        if len(data['last_name']) < 2 :
            is_valid = False
            flash('Your last name must contain at least two characters')

        if len(data['password']) < 5 : #may need to be 8 so check req length
            is_valid = False
            flash('Your password must contain at least 5 characters')

        if data['password'] != data['confirm_password']:
            is_valid = False
            flash('passwords no matchy')

        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Please use valid email address')

        if cls.get_user_by_email(data['email']):
            is_valid = False
            flash('That email is taken')

        return is_valid


    #PARSE USER DATA
    @classmethod
    def instantiate_user(cls, data):
        if 'users.id' in data:
            return(cls({
                'id': data['user.id'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'password': data['password'],
                'created_at': data['user.created_at'],
                'updated_at': data['user.updated_at']  
            }))
        return cls(data)
