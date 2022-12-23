
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User table"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable = False,
    )

class Cocktails(db.Model):
    """Coctail details"""

    __tablename__ = 'cocktail'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    img_url = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    ingredients = db.relationship('ingredient', secondary= 'cocktail_ingredient', backref= 'cocktail')

class Fav(db.Model):
    """users fav cocktails"""

    __tablename__ = 'fav'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete= "cascade"),
    )

    cocktail_id = db.Column(
        db.Integer,
        db.foreignKey('cocktail.id', ondelete= "cascade"),
    )

class Ingredient(db.Model):
    """Ingredient table"""
    __tablename__= 'ingredient'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

class Cocktail_Ingredient(db.Model):
    """cocktail-ingredient middle table"""

    __tablename__ = 'cocktail_ingredient'


    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    cocktail_id = db.Column(
        db.Integer,
        db.Foreignkey('cocktail.id')
    )

    ingredient_id = db.Column(
        db.Integer,
        db.Foreignkey('ingredient.id')
    )

    measurement = db.column(
        db.Text,
        nullable=False
    )

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)