from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_app.models import character_model, user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



#Index page view of registeration form
@app.route('/')
def index():
    return render_template('index.html')


# Create Users on index.html page
@app.route('/users/create', methods=['POST'])
def create_user():
    if user_model.User.create_user(request.form):
        return redirect('/users/home')
    return redirect('/')

# Direct users to home page after registering
@app.route('/users/home')
def home():
    user_id = session.get('user_id')  # Fetch user ID from session
    if user_id is None:
        flash('User not logged in')
        return redirect('/')

    characters = character_model.Character.get_all_character_W_hosts()
    return render_template('home.html', characters=characters)


# LOGIN/OUT
@app.route('/users/login', methods=['POST'])
def login():
    if user_model.User.login(request.form):
        return redirect('/users/home')
    return redirect('/')

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')
