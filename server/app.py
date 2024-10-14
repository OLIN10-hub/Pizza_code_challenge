#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def restaurants():
    restaurants = Restaurant.query.all()
    response = [restaurant.to_dict(only=("id", "name", "address")) for restaurant in restaurants]
    return make_response(response, 200)

@app.route('/restaurants/<int:id>', methods=['GET'])
def restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant:
        response = restaurant.to_dict()
        return make_response(response, 200)
    else:
        return make_response({"error": "Restaurant not found"}, 404)
    
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response({"message": "Restaurant deleted successfully"}, 204)
    else:
        return make_response({"error": "Restaurant not found"}, 404)
    
@app.route('/pizzas', methods=['GET'])
def pizzas():
    pizzas = Pizza.query.all()
    response = [pizza.to_dict(only=("id", "name", "ingredients")) for pizza in pizzas]
    return make_response(response, 200)
    
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    try:
        data = request.get_json() if request.is_json else request.form
        restaurant_pizzas = RestaurantPizza(**data)
        db.session.add(restaurant_pizzas)
        db.session.commit()
        return make_response(restaurant_pizzas.to_dict(), 201)
    except ValueError:
        return make_response({"errors": ["validation errors"]}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)