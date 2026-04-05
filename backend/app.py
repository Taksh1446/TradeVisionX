from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db, cursor
import jwt
import datetime
import bcrypt
import os

app = Flask(__name__)
CORS(app)

# ✅ SECRET KEY FROM ENV
SECRET_KEY = os.getenv("SECRET_KEY")


# ------------------ REGISTER ------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    name = data['name']
    email = data['email']
    password = data['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, balance) VALUES (%s,%s,%s,%s)",
            (name, email, hashed, 10000)
        )
        db.commit()
        return jsonify({"message": "User registered successfully"})
    except:
        return jsonify({"error": "User already exists"}), 400


# ------------------ LOGIN ------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data['email']
    password = data['password']

    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
        token = jwt.encode({
            'user_id': user[0],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# ------------------ PROFILE ------------------
@app.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = data['user_id']

        cursor.execute("SELECT id,name,email,balance FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()

        return jsonify({
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "balance": user[3]
        })

    except:
        return jsonify({"error": "Invalid token"}), 403


# ------------------ BUY STOCK ------------------
@app.route('/buy', methods=['POST'])
def buy_stock():
    data = request.json

    user_id = data['user_id']
    symbol = data['symbol']
    quantity = int(data['quantity'])
    price = float(data['price'])

    total = quantity * price

    cursor.execute("UPDATE users SET balance = balance - %s WHERE id=%s", (total, user_id))

    cursor.execute(
        "INSERT INTO transactions (user_id, stock_symbol, type, quantity, price) VALUES (%s,%s,%s,%s,%s)",
        (user_id, symbol, "BUY", quantity, price)
    )

    db.commit()

    return jsonify({"message": "Stock bought"})


# ------------------ SELL STOCK ------------------
@app.route('/sell', methods=['POST'])
def sell_stock():
    data = request.json

    user_id = data['user_id']
    symbol = data['symbol']
    quantity = int(data['quantity'])
    price = float(data['price'])

    total = quantity * price

    cursor.execute("UPDATE users SET balance = balance + %s WHERE id=%s", (total, user_id))

    cursor.execute(
        "INSERT INTO transactions (user_id, stock_symbol, type, quantity, price) VALUES (%s,%s,%s,%s,%s)",
        (user_id, symbol, "SELL", quantity, price)
    )

    db.commit()

    return jsonify({"message": "Stock sold"})


# ------------------ ROOT ------------------
@app.route('/')
def home():
    return "TradeVisionX API Running 🚀"


# ✅ IMPORTANT: RENDER FIX (PORT + HOST)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
