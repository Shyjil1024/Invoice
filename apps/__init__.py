import os
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/invoice_db")
    app.secret_key = os.getenv("SECRET_KEY", "secretkey")

    mongo.init_app(app)

    # Import and register the routes Blueprint
    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    @app.route('/')
    def home():
        return "Welcome to the Supplier Invoice Management Application!"

    return app
