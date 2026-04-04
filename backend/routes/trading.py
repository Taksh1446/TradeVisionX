from flask import Blueprint, request, jsonify
from db import db, cursor
import yfinance as yf

trading_routes = Blueprint('trading', __name__)

@trading_routes.route('/price/<symbol>', methods=['GET'])
def get_price(symbol):
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")['Close'].iloc[-1]
    return jsonify({"symbol": symbol, "price": float(price)})

@trading_routes.route('/buy', methods=['POST'])
def buy():
    data = request.json
    user_id = data['user_id']
    symbol = data['symbol']
    qty = int(data['qty'])

    stock = yf.Ticker(symbol)
    price = float(stock.history(period="1d")['Close'].iloc[-1])

    total = price * qty

    cursor.execute("SELECT balance FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if user['balance'] < total:
        return jsonify({"error": "Insufficient balance"})

    cursor.execute("UPDATE users SET balance=balance-%s WHERE id=%s", (total, user_id))

    cursor.execute("""
        INSERT INTO portfolio (user_id, stock_symbol, quantity, avg_price)
        VALUES (%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE 
        quantity = quantity + %s
    """, (user_id, symbol, qty, price, qty))

    db.commit()

    return jsonify({"message": "Stock bought"})