from flask_app import app, DB, row_from_db
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import character_model


class Key_Stats:
    def __init__(self, data):
        self.id = data['id'],
        self.str = data['str'],
        self.agy = data['agy'],
        self.sta = data['sta'],
        self.int = data['int'],
        self.int = data['spt'],
        self.cha = data['cha'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at'],
        self.on_character = []

### Pushing data to db for storage ###
    @classmethod
    def save(cls, data):
        query = "INSERT INTO key_stats ( str, agy, sta, int, spt, cha, created_at, updated_at) VALUES (%(str)s, %(agy)s, %(sta)s, %(int)s, %(spt)s, %(cha)s, %(created_at)s, %(updated_at)s NOW(), NOW() );"
        return connectToMySQL('characters').query_db(query, data)
    


### retrieving the stats for the selected character ###
    @classmethod
    def get_stat_with_character (cls, data):
        query = " SELECT * FROM key_stats LEFT JOIN key_stats_has_characters on key_stats_has_characters.key_stats_id = key_stats.id LEFT JOIN characters on key_stats_has_characters.characters_id = characters.id WHERE key_stats.id"
        results = connectToMySQL('characters').query_db(query, data)
        #returning results as a list where added to the character
        character_data = {
            'id' : row_from_db['characters.id'],
            'name' : row_from_db['name'],
            'race' : row_from_db['race'],
            'hp' : row_from_db['hp'],
            'speciality' : row_from_db['speciality'],
            'character_level' : row_from_db['character_level'],
            'created_at' : row_from_db['key_stats.created_at'],
            'updated_at' : row_from_db['key_stats.updated_at']
        }
        key_stats.on_character.append( character.Character(character_data) )