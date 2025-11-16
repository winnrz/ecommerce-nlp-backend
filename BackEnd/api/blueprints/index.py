from flask_cors import cross_origin
from flask import Blueprint
from firebase_admin import db

index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/', methods=['GET'])
@cross_origin()
def index():
    ref = db.reference("/products")
    return (ref.get())