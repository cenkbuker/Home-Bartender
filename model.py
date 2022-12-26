
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
        autoincrement=True
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

    @classmethod
    def register(cls, username, password, first_name, last_name):
        """Register handling, password crypted"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Checks user is valid or not"""

        user = User.query.filter_by(username = username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

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

    instructions = db.Column(
        db.Text,
        nullable=False,
    )

    ingredients = db.relationship('Ingredient', secondary= 'cocktail_ingredient', backref= 'cocktail')

class Fav(db.Model):
    """users fav cocktails"""

    __tablename__ = 'fav'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete= "cascade"),
    )

    cocktail_id = db.Column(
        db.Integer,
        db.ForeignKey('cocktail.id', ondelete= "cascade"),
    )

class Ingredient(db.Model):
    """Ingredient table"""
    __tablename__= 'ingredient'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    ing_name = db.Column(
        db.Text,
        nullable=False,
    )

class Cocktail_Ingredient(db.Model):
    """cocktail-ingredient middle table"""

    __tablename__ = 'cocktail_ingredient'


    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    cocktail_id = db.Column(
        db.Integer,
        db.ForeignKey('cocktail.id')
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey('ingredient.id')
    )

    measurement = db.Column(
        db.Text
    )

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)