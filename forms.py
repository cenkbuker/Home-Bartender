from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""
    first_name = StringField('First name', validators=[DataRequired()] )
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])

class SearchCocktailForm(FlaskForm):
    """Cocktail serach form"""

    name = StringField('Cocktail name', validators=[DataRequired()])

class AddComments(FlaskForm):
    """Form for adding comments"""
    comment= StringField('Your comments', validators=[DataRequired()])
