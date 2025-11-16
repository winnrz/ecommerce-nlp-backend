from flask_cors import cross_origin
from flask import Blueprint, request, jsonify
from firebase_admin import db


place_order_bp = Blueprint('place_order_bp', __name__)


@place_order_bp.route('/checkout', methods=['POST'])
@cross_origin()
def place_order():
    data = request.json
    email = data['email']
    order = data['order']
    amount = data['amount']
    phone_number = data['phoneNumber']
    country = data["country"]
    region = data["region"]
    town = data["town"]
    home_address = data["homeAddress"]
    land_mark = data["landMark"]
    paid = data["paid"]
    date = data["date"]
    progression = request.args.get('progression')
    ref = db.reference("/orders")
    
    # print(progression)

    if progression == "payment":
        try:
            # Push user data to Firebase database
            ref.push(
                {
                    "email": email,
                    "order": order,
                    "amount": amount,
                    "country": country,
                    "phoneNumber": phone_number,
                    "region": region,
                    "town": town,
                    "homeAddress": home_address,
                    "landMark": land_mark,
                    "paid": paid,
                    "date": date,
                })
            return jsonify({'message': 'Order Places Successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500