from flask_app import app, DB
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session, url_for, request, redirect
from flask_app.controllers import character_controller
import re
from flask_bcrypt import Bcrypt
from flask_app.models import user_model
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA]+$')


    #CREATE character
class Character:
        
        def __init__(self, data):
            self.id = data["id"]
            self.user_id = data["user_id"]
            self.name = data["name"]
            self.race = data['race']
            self.hp = data['hp']
            self.speciality = data["speciality"]            
            self.character_level = data['character_level']
            self.created_at = data["created_at"]
            self.updated_at = data["updated_at"]
            self.host = None
            
    



    
    #---@@@ CREATE character MODELS @@@---#
        @classmethod
        def create_character(cls, data):
            if not cls.validate_character_data(data):
                return False

            query = '''
                INSERT INTO characters ( name, race, hp, speciality, character_level, user_id)
                VALUES ( %(name)s, %(race)s, %(hp)s, %(speciality)s, %(character_level)s, %(user_id)s);
                '''

            return connectToMySQL(DB).query_db(query, data)



    #---@@@ READ character MODELS @@@---#
        @classmethod
        def get_all_character_W_hosts(cls):
            query = '''
                SELECT * 
                FROM characters 
                LEFT JOIN user ON user.id = characters.user_id; 
                '''
            results = connectToMySQL(DB).query_db(query)
            characterss = []
            if not results:
                return characterss
            for result in results:
                this_character = cls(result)
                this_character.host = user_model.User.instantiate_user(result)
                characterss.append(this_character)
                print('get_all_characters_W_hosts')
            return characterss



        @classmethod
        def get_character_for_user(cls, data):
            query = '''
                SELECT * 
                FROM characters 
                JOIN user ON user.id = characters.user_id
                WHERE user.id = %(id)s;
                '''
            results = connectToMySQL(DB).query_db(query, data)
            characterss = []
            for result in results:
                this_character = cls(result)
                this_character.host = user_model.User.instantiate_user(result)
                characterss.append(this_character)
            return characterss




    #---@@@ READ ONE SINGLE character MODELS @@@---#
        @classmethod
        def read_one_character(cls, data):
            print(data)
            query = '''
                SELECT * FROM characters JOIN user ON user.id = characters.user_id WHERE characters.id = %(id)s;
                '''
            results = connectToMySQL(DB).query_db(query, data)
            result = results[0]
            character = cls(result)
            character.host = user_model.User.instantiate_user(result)
            return character if result else None
            # return cls(result[0]) if result else None






    #---@@@ FETCH character AND CHECK FOR UNIQUENESS MODELS@@@---#
        @classmethod
        def is_name_unique(cls, name):
            query = '''
                SELECT * 
                FROM characters
                WHERE name = %(name)s
                '''
            result = connectToMySQL(DB).query_db(query, {'name': name})
            return not result  # If the result is empty, the name is unique






    #---@@@ UPDATE character MODELS @@@---#
        @classmethod
        def update_character(cls, data):
            if not cls.validate_character_data(data):
                return False
            
            
            query = '''
                UPDATE characters SET name = %(name)s, race = %(race)s, hp= %(hp)s, character_level = %(character_level)s, speciality = %(speciality)s                     
                WHERE id = %(id)s;
                '''
            connectToMySQL(DB).query_db(query, data)    
            
            flash('character updated successfully', 'success')
            return redirect('/users/home')





    #---@@@ DELETE character MODELS @@@---#
        @classmethod
        def delete_character(cls, data):
            query = '''
                        DELETE FROM characters 
                        WHERE id = %(id)s
                    '''
            results = connectToMySQL(DB).query_db(query, data)

            if results == None:
                return 'Successfully Deleted'
            else:
                return 'Failed to Delete'




        #---@@@ VALIDATION USER @@@---#
        @classmethod
        def validate_character_data(cls, data):
            is_valid = True        

            if len(data['name']) < 2:
                flash('Name must be 2 or more characters')
                is_valid = False

            if len(data['character_level']) < 1:
                flash('Make sure you entered your character level, even intro monsters have a few levels')
                is_valid = False


                
            # date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            # if not date_regex.match(data['release_date']):
            #     flash('Invalid date format, please use YYYY-MM-DD.')
            #     is_valid = False

            

            

            return is_valid



        
