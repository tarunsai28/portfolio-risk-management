#models.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # ✅ Relationship: One Investor → Many Portfolios
    portfolios = db.relationship('Portfolio', back_populates='investor', lazy=True, cascade="all, delete-orphan")


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    investor_id = db.Column(db.Integer, db.ForeignKey('investor.id'), nullable=False)
    value = db.Column(db.Float, default=0.0)  # Ensure this exists

    # ✅ Fix Relationship (Avoid Redundant `backref`)
    investor = db.relationship('Investor', back_populates='portfolios')


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
