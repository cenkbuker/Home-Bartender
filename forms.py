from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField
from wtforms.validators import DataRequired, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])

class SearchCocktailForm(FlaskForm):
    """Cocktail serach form"""

    name = StringField('Cocktail name', validators=[DataRequired()])
    choice = RadioField("Cocktail name or ingredient?", choices=[('cocktails','cocktails'),('ingredients','ingredients')], default='cocktails')

class UserNewCocktailForm(FlaskForm):
    """Form for adding users."""
    name = StringField('Cocktail name', validators=[DataRequired()])
    photo = StringField('Cocktail photo', validators=[DataRequired()])
    description = StringField('Cocktail description')
   
