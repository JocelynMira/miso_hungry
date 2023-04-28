from flask_app import app
from flask import render_template, session, redirect, request, flash
from flask_app.models.user_model import User
from flask_app.models.dish_model import Dish

@app.route('/add_dish')
def add_dish():
    if 'user_id' not in session:
        redirect ('/logout')
    else:
        data = {
            'id': session['user_id']
        }
    return render_template ('/new_dish.html', user = User.get_user_by_id(data))

# CREATE
@app.route('/new_dish', methods= ['POST'])
def post_dish():
    if 'user_id' not in session:
        redirect ('/logout')
    if not Dish.validate_dish(request.form):
        return redirect ('/add_dish')
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "price": request.form['price'],
        "quantity": request.form['quantity'],
        "user_id": session['user_id']
    }
    print(data)
    Dish.save(data)
    return redirect ('/dashboard')

# READ
@app.route('/all_dishs')
def all_dishs():
    if 'user_id' not in session:
        return redirect ('/logout')
    return redirect ('/dashboard')

@app.route('/display_dish/<int:id>')
def one_dish(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    else:
        data = {
            'id':id
        }
        user_data = {
            'id' : session['user_id']
        }
    return render_template ('show_dish.html', one_dish = Dish.get_dish_by_id(data), user = User.get_user_by_id(user_data), all_users = User.get_all())

# UPDATE
@app.route('/update_dish', methods=['POST'])
def update_dish():
    if 'user_id' not in session:
        redirect ('/logout')
    if not Dish.validate_dish(request.form):
        return redirect ('/add_dish')
    data = {
        "title": request.form['title'],
        "description": request.form['description'],
        "price": request.form['price'],
        "quantity": request.form['quantity'],
        "user_id": session['user_id']
    }
    Dish.update_dish(data)
    return redirect ('/dashboard')

@app.route('/edit_dish/<int:id>')
def edit_dish(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template ('update_dish.html', one_dish = Dish.get_dish_by_id(data), user = User.get_user_by_id(user_data))

# DELETE
@app.route('/delete_dish/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    Dish.delete(id)
    return redirect ('/dashboard')



