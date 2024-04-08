from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        serialized_plants = [plant.serialize() for plant in plants]
        return make_response(jsonify(serialized_plants), 200)

    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "No data provided"}), 400)
        name = data.get('name')
        if not name:
            return make_response(jsonify({"error": "Name is required"}), 400)

        image = data.get('image')

        new_plant = Plant(name=name, image=image, price=data.get('price'))
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.serialize()), 201


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        return jsonify(plant.serialize())


api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
