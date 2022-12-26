from flask import Flask, render_template, request, flash, redirect, session, g, abort
import requests
from functions import add_cocktail
from model import db, connect_db, User, Cocktails, Cocktail_Ingredient, Fav, Ingredient
from forms import UserAddForm, LoginForm, SearchCocktailForm, UserNewCocktailForm

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bartender'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "capstonesecret"


BASE_API_URL = 'https://www.thecocktaildb.com/api/json/v2/1/'
CURR_USER_KEY = "curr_user"

@app.route('/', methods = ["POST", "GET"])
def homepage():

    form = SearchCocktailForm()
    if form.validate_on_submit():
        name = form.name.data
        choice = form.choice.data
        return redirect(f'/{choice}/{name}')
    return render_template("homepage.html", form=form)

@app.route('/cocktails/<int:id>', methods=['GET','POST'])
def coctail_details(id):
    data = requests.get(f"{BASE_API_URL}lookup.php?i={id}").json()
    add_cocktail(data)
    cocktail = Cocktails.query.filter_by(id= id).first()
    measurement = Cocktail_Ingredient.query.filter_by(cocktail_id = id).all()
    return render_template('cocktail-details.html', cocktail=cocktail, measurement=measurement )


@app.route('/cocktails/<string:name>')
def search_cocktail(name):
    data = requests.get(f"{BASE_API_URL}search.php?s={name}").json()
    for result in data:
        search_cocktail(result)
        searched_cocktails= Cocktails.query.filter(Cocktails.name.like('%' + name + '%'))
    return render_template('search-list.html',name=name, cocktails=searched_cocktails)


#USER LOGIN AND REGISTER

@app.route('/login', methods=['GET','POST'])
def login_user():
    """User login handling"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username,password)
        if user:
            session[CURR_USER_KEY] = user.id
            return redirect('/')
        else:
            form.username.errors = ['Invalid Username/Passwords']
    
    return render_template('login.html', form = form)


@app.route('/register', methods=["GET", 'POST'])
def register_user():
    """User register handling"""
    form = UserAddForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password,first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session[CURR_USER_KEY] = user.id
        flash("User Created","success")
        return redirect('/')
    else:
        return render_template('register.html', form=form)       
    

@app.route('/logout')
def logout():
    session.pop(CURR_USER_KEY)
    flash("You have logged out successfully",'success')
    return redirect('/')

###########