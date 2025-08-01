import os
from flask_admin import Admin
from models import db, User, Character, Favorites, Planet, Vehicle
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    class UserView(ModelView):
        column_list = ('id', 'username', 'email', 'favorites')
        form_columns = ('username', 'email', 'password')

    class CharacterView(ModelView):
        column_list = ('id', 'name', 'homeworld_id')
        form_columns = ('name', 'homeworld_id')
        
    class PlanetView(ModelView):
        column_list = ('id', 'name', 'size', 'biome_type')
        form_columns = ('name', 'size', 'biome_type')
        
    class VehicleView(ModelView):
        column_list = ('id', 'name', 'manufacturing_planet_id', 'character_owner_id')
        form_columns = ('name', 'manufacturing_planet_id', 'character_owner_id')
    
    class FavoriteView(ModelView):
        column_list = ('id', 'user_id', 'character_id', 'planet_id', 'vehicle_id')
        form_columns = ('user_id', 'character_id', 'planet_id', 'vehicle_id')


    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserView(User, db.session))
    admin.add_view(CharacterView(Character, db.session))
    admin.add_view(PlanetView(Planet, db.session))
    admin.add_view(VehicleView(Vehicle, db.session))
    admin.add_view(FavoriteView(Favorites, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
