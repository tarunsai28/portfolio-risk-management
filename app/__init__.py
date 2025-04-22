#__init__.py
import os
from flask import Flask, app
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager  # ✅ Import JWTManager
from app.routes import routes  

db = SQLAlchemy()
jwt = JWTManager()  # ✅ Create JWTManager instance

def create_app():
    app = Flask(__name__)
    
    # ✅ Allow frontend (React) access
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

    # Ensure instance folder exists
    os.makedirs("instance", exist_ok=True)

    # Database setup
    db_path = os.path.abspath(os.path.join("instance", "portfolio.db"))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'  # ✅ Required for JWT
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # ✅ Set JWT secret key

    db.init_app(app)
    jwt.init_app(app)  # ✅ Initialize JWTManager
    Migrate(app, db)

    # ✅ Ensure database exists
    with app.app_context():
        if not os.path.exists(db_path):
            print("🔹 Creating database file...")
            open(db_path, 'w').close()
        db.create_all()
        print("✅ Database initialized!")

    from app.routes import routes  # Import routes
    app.register_blueprint(routes)

    return app
