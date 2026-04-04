from flask import Flask
from flask_cors import CORS
from routes.auth import auth_routes
from routes.trading import trading_routes
from routes.portfolio import portfolio_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_routes)
app.register_blueprint(trading_routes)
app.register_blueprint(portfolio_routes)

@app.route('/')
def home():
    return "TradeVisionX API Running 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)