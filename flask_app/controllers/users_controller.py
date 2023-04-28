from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.user_model import User
from flask_app.models.painting_model import Painting

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # if user isnt logged in, bring them to register page
    if 'user_id' not in session:
        return render_template ('register.html')
    else:
        return redirect ('/dashboard')

@app.route('/register', methods= ["POST"])
def register():
    # if user IS NOT validated, redirect them back and let them know
    if not User.validate_registration(request.form):
        return redirect ('/')
    # if user IS validated, save the data they input and hash password
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    # check for errors, if all went well, put user in session
    if not id:
        flash('Something went wrong')
    else:
        session['user_id'] = id
        flash("Success! You're now registered.")
        return redirect ('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in or register.')
        return redirect ('/logout')
    else:
        data = {
            'id' : session['user_id']
        }
        return render_template ('dashboard.html', users = User.get_all, all_paintings = Painting.get_all(), user = User.get_user_by_id(data))

# user login/ LOGIN VALIDATIONS
@app.route('/login', methods = ['POST'])
def login():
    data = {
        'email' : request.form['email']
    }
    # check if the email is in database
    user = User.get_user_by_email(data)
    if not user:
        # email must already exist in the database
        flash('Email not found. Please register.', "login")
        return redirect ('/')
        # password must be checked against the hashed password in database for existing user
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password', "login")
        return redirect ('/')
    else:
        session['user_id'] = user.id
        flash('You are now logged in',"login")
        return redirect ('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash("You're now logged out.")
    return redirect ('/')