from flask import Flask

app = Flask(__name__)
app.secret_key = 'root'

# DataBase name 
DB = 'dnd_digital_card'

print('Flask app spinned up successefully!')
