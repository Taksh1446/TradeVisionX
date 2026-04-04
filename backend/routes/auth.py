from flask import Blueprint, request, jsonify
from db import db, cursor
import bcrypt
import jwt
import datetime

auth_routes = Blueprint('auth', __name__)

SECRET_KEY = "secret123"

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO users (name,email,password,balance) VALUES (%s,%s,%s,%s)",
                   (name, email, password, 100000))
    db.commit()

    return jsonify({"message": "User registered"})

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = jwt.encode({
            "user_id": user['id'],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401