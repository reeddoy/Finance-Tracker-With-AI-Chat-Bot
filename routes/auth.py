from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import User, db



auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    existing_user_by_username = User.query.filter_by(username=data['username']).first()

    if existing_user_by_username:
        return jsonify({"error": "Username already exists"}), 400

    existing_user_by_email = User.query.filter_by(email=data['email']).first()
    if existing_user_by_email:
        return jsonify({"error": "Email already exists"}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "registerd_successfull"})



@auth.route('/login', methods=['POST'])
def login():
    data = request.json

    user = None
    if "@" in data['email']:  # If the input contains an '@', treat it as an email
        user = User.query.filter_by(email=data['email']).first()
    else:  # Otherwise, treat it as a username
        user = User.query.filter_by(username=data['email']).first()

    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        # Generate access token with expiration (15 minutes)
        access_token = create_access_token(identity=str(user.id), fresh=True)
        
        # Generate a refresh token with longer expiration (7 days)
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })
    
    return jsonify({"error": "Invalid credentials"}), 401



@auth.route('/verify-token', methods=['POST'])
@jwt_required()
def verify_token():
    current_user = get_jwt_identity()
    return jsonify({"message": "Token_valid"}), 200



@auth.route('/refresh-token', methods=['POST'])
@jwt_required(refresh=True)  
def refresh_token():
    current_user = get_jwt_identity()

    new_access_token = create_access_token(identity=str(current_user))
    
    return jsonify({
        "access_token": new_access_token
    }), 200