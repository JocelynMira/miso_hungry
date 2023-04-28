from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user_model import User


class Dish:
    
    DB= "miso_hungry_db"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.image_name = data['image_name']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # CREATE
    @classmethod
    def save(cls, data):
        query = """INSERT INTO dishes (name, image_name, description, price, user_id) VALUES ( %(name)s, %(image_name)s, %(description)s, %(price)s, %(user_id)s )"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    # READ
    @classmethod
    def get_all_orders(cls):
        query = """SELECT * FROM dishes
                LEFT JOIN users ON dishes.user_id = users.id
                """
        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        order = []

        for dish in results:
            one_dish = cls(dish)
            customer = {
                'id': dish['users.id'],
                'first_name': dish['first_name'],
                'last_name': dish['last_name'],
                'email': dish['email'],
                'password': dish['password'],
                'created_at': dish['users.created_at'],
                'updated_at': dish['users.updated_at'],
            }
            one_dish.user = User(customer)
            order.append(one_dish)
        return order
    
    @classmethod
    def get_dish_by_id(cls, data):
        query = """SELECT * FROM dishes
                WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    #UPDATE
    @classmethod
    def update_dish(cls,data):
        query = """UPDATE dishes SET
                dish_id= %(dish_id)s, description = %(description)s, price = %(price)s"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return results


    # DELETE
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM dishes WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})
        return results

