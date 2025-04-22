#routes.py
import os
from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models import Investor, Portfolio, Asset, User
from flask import request, jsonify
import joblib
import numpy as np
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

routes = Blueprint('routes', __name__)

### 📌 INVESTOR ENDPOINTS ###

# Create an investor
@routes.route('/api/investor', methods=['POST'])
def add_investor():
    from app import db  
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Name and email are required"}), 400

    investor = Investor(name=data['name'], email=data['email'])
    db.session.add(investor)
    db.session.commit()
    
    return jsonify({"message": "Investor added successfully!", "id": investor.id}), 201

# Get all investors
@routes.route('/api/investors', methods=['GET'])
def get_investors():
    investors = Investor.query.all()
    return jsonify([{"id": inv.id, "name": inv.name, "email": inv.email} for inv in investors]), 200

# Update an investor
@routes.route('/api/investor/<int:id>', methods=['PUT'])
def update_investor(id):
    from app import db  
    investor = Investor.query.get(id)
    if not investor:
        return jsonify({"error": "Investor not found"}), 404

    data = request.get_json()
    investor.name = data.get('name', investor.name)
    investor.email = data.get('email', investor.email)
    db.session.commit()
    
    return jsonify({"message": "Investor updated successfully!"}), 200

# Delete an investor
@routes.route('/api/investor/<int:id>', methods=['DELETE'])
def delete_investor(id):
    from app import db  
    investor = Investor.query.get(id)
    if not investor:
        return jsonify({"error": "Investor not found"}), 404

    db.session.delete(investor)
    db.session.commit()
    return jsonify({"message": "Investor deleted successfully!"}), 200


### 📌 PORTFOLIO ENDPOINTS ###

# Create a portfolio for an investor
@routes.route('/api/portfolio', methods=['POST'])
def add_portfolio():
    from app import db  
    data = request.get_json()
    if 'name' not in data or 'investor_id' not in data:
        return jsonify({"error": "Portfolio name and investor_id are required"}), 400

    investor = Investor.query.get(data['investor_id'])
    if not investor:
        return jsonify({"error": "Investor not found"}), 404

    portfolio = Portfolio(name=data['name'], investor_id=data['investor_id'])
    db.session.add(portfolio)
    db.session.commit()
    
    return jsonify({"message": "Portfolio created successfully!", "id": portfolio.id}), 201

# Get all portfolios for an investor
@routes.route('/api/investor/<int:id>/portfolios', methods=['GET'])
def get_investor_portfolios(id):
    investor = Investor.query.get(id)
    if not investor:
        return jsonify({"error": "Investor not found"}), 404

    portfolios = Portfolio.query.filter_by(investor_id=id).all()
    return jsonify([{"id": p.id, "name": p.name} for p in portfolios]), 200

# Delete a portfolio
@routes.route('/api/portfolio/<int:id>', methods=['DELETE'])
def delete_portfolio(id):
    from app import db  
    portfolio = Portfolio.query.get(id)
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404

    db.session.delete(portfolio)
    db.session.commit()
    return jsonify({"message": "Portfolio deleted successfully!"}), 200


### 📌 ASSET ENDPOINTS ###

# Add an asset to a portfolio
@routes.route('/api/asset', methods=['POST'])
def add_asset():
    from app import db  
    data = request.get_json()
    if 'name' not in data or 'type' not in data or 'value' not in data or 'portfolio_id' not in data:
        return jsonify({"error": "Asset name, type, value, and portfolio_id are required"}), 400

    portfolio = Portfolio.query.get(data['portfolio_id'])
    if not portfolio:
        return jsonify({"error": "Portfolio not found"}), 404

    asset = Asset(name=data['name'], type=data['type'], value=data['value'], portfolio_id=data['portfolio_id'])
    db.session.add(asset)
    db.session.commit()
    
    return jsonify({"message": "Asset added successfully!", "id": asset.id}), 201

### 📌 Portfolio Summary Endpoint ###
@routes.route('/api/portfolio_summary', methods=['GET'])
@jwt_required()
def portfolio_summary():
    user_id = get_jwt_identity()  # Get logged-in user ID
    investor = Investor.query.filter_by(id=user_id).first()  # Fix lookup

    if not investor:
        return jsonify({"error": "Investor not found"}), 404

    portfolios = Portfolio.query.filter_by(investor_id=investor.id).all()
    
    if not portfolios:
        return jsonify({"error": "No portfolios found for this investor"}), 404

    total_value = sum(portfolio.value for portfolio in portfolios) if portfolios else 0

    # Simulated Performance Data
    performance = [
        {"date": "2025-01-01", "value": total_value * 0.95},
        {"date": "2025-02-01", "value": total_value * 1.02},
        {"date": "2025-03-01", "value": total_value * 1.08},
    ]

    # Example Asset Allocation
    assets = [
        {"name": "Stocks", "allocation": 40},
        {"name": "Bonds", "allocation": 25},
        {"name": "Crypto", "allocation": 20},
        {"name": "Real Estate", "allocation": 15},
    ]

    risk_level = "Medium" if total_value < 100000 else "High"

    return jsonify({
        "total_value": total_value,
        "risk_level": risk_level,
        "performance": performance,
        "assets": assets
    }), 200
# Delete an asset
@routes.route('/api/asset/<int:id>', methods=['DELETE'])
def delete_asset(id):
    from app import db  
    asset = Asset.query.get(id)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404

    db.session.delete(asset)
    db.session.commit()
    return jsonify({"message": "Asset deleted successfully!"}), 200


# ✅ User Registration
@routes.route('/api/register', methods=['POST'])
@cross_origin(origin="http://localhost:3000", supports_credentials=True)
def register():
    from app import db
    from app.models import User

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # ✅ Check if the username or email already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already taken. Choose another one."}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered. Try logging in."}), 400

    # ✅ Create a new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error. Please try again."}), 500




@routes.route('/api/login', methods=['POST', 'OPTIONS'])
@cross_origin(origin="http://localhost:3000", supports_credentials=True)
def login():
    from app import db
    from app.models import User
    from flask import current_app  # Import Flask's current_app

    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight successful"}), 200

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    print(f"📩 Login attempt for: {email}")

    with current_app.app_context():  # Ensure the Flask app context is active
        user = User.query.filter_by(email=email).first()
        if not user:
            print("❌ User not found!")
            return jsonify({"error": "Invalid email or password"}), 401

        print(f"🔑 Stored Hash: {user.password_hash}")
        print(f"🔑 Entered Password: {password}")

        if not user.check_password(password):
            print("❌ Password does not match!")
            return jsonify({"error": "Invalid email or password"}), 401

        print("✅ Login successful!")
        access_token = create_access_token(identity=str(user.id))

    return jsonify({"token": access_token, "message": "Login successful"}), 200





# ✅ Protected Route Example
@routes.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, User {current_user}!"}), 200



# Load Trained Model
model = joblib.load("app/ml/risk_model.pkl")

from flask import current_app

@routes.route('/api/predict_risk', methods=['POST'])
def predict_risk():
    data = request.get_json()
    volatility = data.get('volatility')
    expected_return = data.get('expected_return')

    if volatility is None or expected_return is None:
        return jsonify({'error': 'Missing data for volatility or expected return'}), 400

    # ✅ Load model dynamically inside function
    model_path = "app/ml/risk_model.pkl"
    if not os.path.exists(model_path):
        return jsonify({'error': 'Model file not found'}), 500

    model = joblib.load(model_path)
    risk_level = model.predict([[volatility, expected_return]])[0]

    return jsonify({'risk_level': risk_level})

