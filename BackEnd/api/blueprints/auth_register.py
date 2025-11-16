from flask_cors import cross_origin
from flask import request, jsonify, session, Blueprint
from flask_jwt_extended import create_access_token
from firebase_admin import db
import pyrebase 
import re
import os
from dotenv import load_dotenv

load_dotenv()

auth_register_bp = Blueprint('auth_register_bp', __name__)

config = {
	"type": "service_account",
	"apiKey": os.getenv("FIREBASE_API_KEY"),
	"authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
	"project_id": os.getenv("FIREBASE_PROJECT_ID"),
	"private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
	"private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
	"client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
	"client_id": os.getenv("FIREBASE_CLIENT_ID"),
	"auth_uri": os.getenv("FIREBASE_AUTH_URI"),
	"token_uri": os.getenv("FIREBASE_TOKEN_URI"),
	"auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),
	"client_x509_cert_url": os.getenv("FIREBASE_CLIENT_CERT_URL"),
	"universe_domain": "googleapis.com",
	"storageBucket": "madbisecommerce.appspot.com",
	"messagingSenderId": "402924060072",
	"appId": "1:402924060072:web:8d8022c71bfedf5e29719d",
	"measurementId": "G-VTW3ZB4PGH",
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@auth_register_bp.route('/auth/register', methods=['POST'])
@cross_origin()
def register():
    data = request.json
    name = data["name"]
    email = data['email']
    password = data["password"]
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    ref = db.reference('/users')

    if (re.match(pattern, email) == None):
        return jsonify({"message": "INVALID_EMAIL"}), 400

    try:
        user = auth.create_user_with_email_and_password(email, password)
        ref.child(name).set({'email': email,})
        return jsonify({"message": "SUCCESS", "uid": user}), 200
    except Exception as e:
        return jsonify({"message": "USER_EXISTS", "error": str(e)}), 400
    
  
@auth_register_bp.route('/auth/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    email = data['email']
    password = data["password"]
    ref = db.reference('/tokens')

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return jsonify({"message": "SUCCESS", "user": user}), 200
    except Exception as e:
        return jsonify({"message": "ERROR", "error": str(e)}), 400
    