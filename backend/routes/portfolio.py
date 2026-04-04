from flask import Blueprint, jsonify
from db import cursor

portfolio_routes = Blueprint('portfolio', __name__)

@portfolio_routes.route('/portfolio/<int:user_id>')
def portfolio(user_id):
    cursor.execute("SELECT * FROM portfolio WHERE user_id=%s", (user_id,))
    data = cursor.fetchall()
    return jsonify(data)