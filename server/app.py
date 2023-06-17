#!/usr/bin/env python3

from flask import Flask, abort, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route("/")
def welcome():
    return "<h1>Welcome to Plantsy!</h1>"


class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants, 200)
    
    def post(self):
# below line is just for lab
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )
    # below lines are if not using the data=request.get_json()
        # new_plant = Plants(
        #     name=request.form['name'],
        #     image=request.form['image'],
        #     price=request.form['price']
        # )
        db.session.add(new_plant)
        db.session.commit()

        response_dict = new_plant.to_dict()

        return make_response(new_plant.to_dict(), 201)
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        if plant:= Plant.query.get(id):
            return make_response(plant.to_dict(), 200)
        else:
            abort(404, f"Could not find Plant with id {id}")

api.add_resource(PlantByID, "/plants/<int:id>")
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
