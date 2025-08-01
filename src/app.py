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
from models import db, User, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
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

# Instancia de objetos
users = User()
characters = Character()

# Obtener todos los users
@app.route('/user', methods=['GET'])
def list_all_users():

    try:
        user_list = users.query.all()
        # user_list = users.serialize()
        """ response_body = user_list

        if user_list is None:
            return jsonify({"Error": "The user does not exist"}), 400 """
        return jsonify([user.serialize() for user in user_list]), 200
    
    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500
    
# Obtener todos los characters
@app.route('/character', methods=['GET'])
def list_all_characters():

    try:
        # char_list = characters.get_all_characters()
        # char_list = characters.serialize()
        response_body = char_list

        if char_list is None:
            return jsonify({"Error": "The character does not exist"}), 400
        return jsonify(response_body), 200
    
    except Exception as e:
        return jsonify({"Error": "Server error", "Message": str(e)}), 500




# Para los favoritos del user ---> query_user = db.session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
