"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Favorites
from sqlalchemy import select
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Instancia de objetos - solo se usará para el método POST (crear nuevo registro en las tablas)
""" users = User()
characters = Character()
planets = Planet()
vehicles = Vehicle()
favorites = Favorites() """

# OBTENER TODOS -----------------------------------------------------------------------------------------------------------------------------------------
# Obtener todos los users

@app.route('/user', methods=['GET'])
def list_all_users():

    try:
        query_results = db.session.execute(select(User)).scalars().all()
        results = list(map(lambda user: user.serialize(), query_results))

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500

# Obtener todos los characters
@app.route('/character', methods=['GET'])
def list_all_characters():

    try:
        query_results = db.session.execute(select(Character)).scalars().all()
        results = list(
            map(lambda character: character.serialize(), query_results))

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500

# Obtener todos los planetas
@app.route('/planet', methods=['GET'])
def list_all_planets():

    try:
        query_results = db.session.execute(select(Planet)).scalars().all()
        results = list(map(lambda planet: planet.serialize(), query_results))

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# Obtener todos los vehiculos
@app.route('/vehicle', methods=['GET'])
def list_all_vehicles():

    try:
        query_results = db.session.execute(select(Vehicle)).scalars().all()
        results = list(map(lambda vehicle: vehicle.serialize(), query_results))

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# Obtener todos los favoritos de un user
@app.route('/favorites/<int:user_id>', methods=['GET'])
def list_all_favorites_from_user(user_id):

    try:
        query_results = db.session.execute(
            select(Favorites).where(Favorites.user_id == user_id)).scalars().all()
        results = list(map(lambda user: user.serialize(), query_results))
        
        return jsonify(results), 200
        

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# OBTENER UNO, POR ID -----------------------------------------------------------------------------------------------------------------------------------------
# Obtener un user
@app.route('/user/<int:user_id>', methods=['GET'])
def list_one_user(user_id):

    try:
        query_results = db.session.execute(
            select(User).where(User.id == user_id)).scalar_one()
        return jsonify(query_results.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# Obtener un character
@app.route('/character/<int:character_id>', methods=['GET'])
def list_one_character(character_id):

    try:
        query_results = db.session.execute(select(Character).where(
            Character.id == character_id)).scalar_one()
        return jsonify(query_results.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# Obtener un planet
@app.route('/planet/<int:planet_id>', methods=['GET'])
def list_one_planet(planet_id):

    try:
        query_results = db.session.execute(
            select(Planet).where(Planet.id == planet_id)).scalar_one()
        return jsonify(query_results.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# Obtener un vehicle
@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def list_one_vehicle(vehicle_id):

    try:
        query_results = db.session.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)).scalar_one()
        return jsonify(query_results.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500



# MÉTODOS POST -----------------------------------------------------------------------------------------------------------------------------------------
# Añade un nuevo character favorito al usuario actual con el id
@app.route('/favorite/character', methods=['POST'])
def add_fav_character():

    try:
        data = request.json
        print(data)

        favorite = Favorites(
            user_id=data["user_id"], character_id=data["character_id"], planet_id=None, vehicle_id=None)
        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# Añade un nuevo planet favorito al usuario actual con el id
@app.route('/favorite/planet', methods=['POST'])
def add_fav_planet():

    try:

        data = request.json
        favorite = Favorites(
            user_id=data["user_id"], character_id=None, planet_id=data["planet_id"], vehicle_id=None)
        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500


# Añade un nuevo vehicle favorito al usuario actual con el id
@app.route('/favorite/vehicle', methods=['POST'])
def add_fav_vehicle():
    try:

        data = request.json
        favorite = Favorites(
            user_id=data["user_id"], character_id=None, planet_id=None, vehicle_id=data["vehicle_id"])
        db.session.add(favorite)
        db.session.commit()

        return jsonify(favorite.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500



# MÉTODOS delete -----------------------------------------------------------------------------------------------------------------------------------------
# Elimina un character de la lista de favoritos del usuario actual
@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def remove_fav_character(character_id):

    try:
        data = request.json
        print(data)

        # favorite = Favorites(
        #     user_id=data["user_id"], character_id=data["character_id"], planet_id=None, vehicle_id=None)
        # db.session.add(favorite)
        # db.session.commit()

        favorite = db.session.get(Favorites, character_id) 
        db.session.delete(favorite)
        db.session.commit()


        return jsonify(favorite.serialize()), 200

    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
