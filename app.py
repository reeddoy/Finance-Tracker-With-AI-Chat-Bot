from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from routes.auth import auth
from routes.expense import expense
from routes.budget import budget
from routes.home import home_route
from routes.category import category
from flask_cors import CORS 

app = Flask(__name__)
app.config.from_object(Config)

CORS(app) #Enable cros app

db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Register Blueprints
app.register_blueprint(home_route)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(expense, url_prefix='/api')
app.register_blueprint(budget, url_prefix='/api')
app.register_blueprint(category, url_prefix='/api')

# Create tables if not exists
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
