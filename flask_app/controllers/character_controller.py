from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash, url_for
# from flask_app.models import character_model, user_model
from flask_app.models.character_model import Character
from flask_app.models.user_model import User
from flask_app.models.key_stats_model import Key_Stats

# CREATE ADVENTURE CONTROLLER
@app.route('/character/create/', methods=['GET'])
def create_page():
    user_id = session.get('user_id')  # Fetch user ID from session
    if user_id is None:
        flash('User not logged in')
        return redirect('/')
    return render_template('Createcharacter.html')



@app.route('/character/create/', methods=['POST'])
def create_character():
    data = {**request.form, 
            'user_id': session.get('user_id')
            }
    if Character.create_character(data):
        return redirect('/character/view/<int:character_id>/')
    else:
        flash('Could not register character, please try again later')
        return redirect('/character/create')



#------------------- SECTION CHANGE ---------------#


# READ character CONTROLLER
@app.route('/character/view/<int:character_id>')
def view_character(character_id):
    if 'user_id' not in session:
        flash('Login to view this page')
        session.clear()
        return redirect('/')

    data = {
        'id': character_id
    }
    Key_Stats.get_stat_with_character(data)



    character = Character.read_one_character(data)

    return render_template('ViewCharacter.html', character=character)






#------------------- SECTION CHANGE ---------------#


# -@@@@@ UPDATE character PAGE @@@@@@-
@app.route('/character/edit/<int:character_id>', methods=['GET'])
def show_edit_character(character_id):
    if 'user_id' not in session:
        flash('Login to view this page')
        session.clear()
        return redirect('/')

    data = {
        'id': character_id
    }



    character = Character.read_one_character(data)

    return render_template('edit_character.html', character=character)


#! Route to update a single character
@app.route('/character/edit/<int:character_id>', methods=['POST'])
def update_single_character(character_id):
    character_data = {
        'id': character_id,
        'user_id': session['user_id'],
        'name': request.form['name'],
        'race':request.form['race'],       
        'hp':request.form['hp'],  
        'character_level' : request.form['character_level'],    
        'speciality' : request.form['speciality']    
    }
        
        
                
    Character.update_character(character_data)
    flash('character updated successfully', 'success')
    return redirect('/users/home')
    






#------------------- SECTION CHANGE ---------------#






# DELETE ADVENTURE CONTROLLER
@app.route('/character/delete/<int:character_id>')
def delete_character(character_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash('Login to view this page')
        session.clear()
        return redirect('/')

    this_character = {
        'id': character_id,
        'user_id': session['user_id']
    }

    Character.delete_character(this_character)

    return redirect('/users/home')


#------------------- SECTION CHANGE ---------------#



# Route to display character details and increase button
@app.route('/character/view/<int:character_id>', endpoint='view_single_character')
def view_character(character_id):
    if 'user_id' not in session:
        flash('Login to view this page')
        session.clear()
        return redirect('/')

    user_id = session['user_id']

    current_user = User.get_user_by_id(user_id)  

    characters = Character.get_all_characters_W_hosts()
    selected_character = next((character for character in characters if character.id == character_id), None)

    if selected_character:
        return render_template('ViewCharacter.html', character=selected_character, current_user=current_user)
    else:
        flash('character not found')
        return redirect('/')