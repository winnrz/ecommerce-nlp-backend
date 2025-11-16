import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# views import
from .blueprints.index import index_bp
from .blueprints.recommendations import recommendations_bp
from .blueprints.auth_register import auth_register_bp
from .blueprints.place_order import place_order_bp

#************************************* FIREBASE *********************************************#
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS"))

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
})


#************************************* PYTHON *********************************************#
#Activate Flask Venv: . .venv/bin/activate  
# flask --app __init__.py run

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"), 
    )

    app.config['CORS_HEADERS'] = 'Content-Type'
    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    jwt = JWTManager(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

#************************************* BLUEPRINTS *********************************************#
    app.register_blueprint(index_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(auth_register_bp)
    app.register_blueprint(place_order_bp)

    return app
