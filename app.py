from flask import Flask, render_template, request, flash, redirect, session, g, abort
import requests
from functions import add_cocktail, search_cocktail, process_cocktail
from model import db, connect_db, User, Cocktails, Cocktail_Ingredient, Fav, Comment
from forms import UserAddForm, LoginForm, SearchCocktailForm, AddComments
import os
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///bartender').replace("://", "ql://", 1)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)
db.create_all()

app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY','capstonesecret')


BASE_API_URL = "https://www.thecocktaildb.com/api/json/v1/1/"
CURR_USER_KEY = "curr_user"


@app.route("/", methods=["POST", "GET"])
def homepage():

    form = SearchCocktailForm()
    if form.validate_on_submit():
        name = form.name.data
        
        return redirect(f"/cocktails/{name}")

    random = requests.get(f"{BASE_API_URL}random.php").json()
    raw_cocktail = random["drinks"][0]
    random_cocktail=process_cocktail(raw_cocktail)
    
    return render_template("homepage.html", form=form, cocktail=random_cocktail)


@app.route("/cocktails/<int:id>", methods=["GET", "POST"])
def coctail_details(id):
    data = requests.get(f"{BASE_API_URL}lookup.php?i={id}").json()
    raw_cocktail = data["drinks"][0]
    processed_cocktail = process_cocktail(raw_cocktail)
    add_cocktail(processed_cocktail)
    cocktail = Cocktails.query.filter_by(id=id).first()
    measurement = Cocktail_Ingredient.query.filter_by(cocktail_id=id).all()
    try:
        form = AddComments()
        if form.validate_on_submit():
            comment = form.comment.data
            new_comment = Comment(user_id = session[CURR_USER_KEY], comment= comment, cocktail_id= id)
            db.session.add(new_comment)
            db.session.commit()
            comments= Comment.query.filter_by(cocktail_id=id).all()
        return render_template(
        "cocktail-details.html", cocktail=cocktail, measurement=measurement, form=form, comments=comments
        )
    except: 
        comments= Comment.query.filter_by(cocktail_id=id).all()
        return render_template(
        "cocktail-details.html", cocktail=cocktail, measurement=measurement, form=form, comments=comments
        )

@app.route("/delete/comment/<int:id>", methods=["POST"])
def delete_comment(id):
    comment= Comment.query.filter_by(id=id).first()
    cocktail_id = comment.cocktail_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(f'/cocktails/{cocktail_id}')

@app.route("/cocktails/<string:name>")
def search_cocktails(name):
    try:
        data = requests.get(f"{BASE_API_URL}search.php?s={name}").json()
        raw_data = data["drinks"]
        return render_template("search-list.html", name=name, cocktails=search_cocktail(raw_data))
    except:
        no_result_dict = {
        "name": "No result for search term",
        }
        return render_template("search-list.html", name=name, cocktails=no_result_dict)

    

# FAV HANDLING

@app.route('/cocktail/<int:fav_cocktail>/fav')
def add_to_fav(fav_cocktail):
    if CURR_USER_KEY not in session:
        return redirect('/login')
    if not Fav.query.filter(Fav.user_id== session[CURR_USER_KEY], Fav.cocktail_id== fav_cocktail).first():
        fav_handle= Fav(user_id= session[CURR_USER_KEY], cocktail_id= fav_cocktail)
        db.session.add(fav_handle)
        db.session.commit()
    return redirect(f'/{session[CURR_USER_KEY]}/favorites')



@app.route('/<int:user_id>/favorites')
def user_fav(user_id):
    if CURR_USER_KEY not in session:
        return redirect('/login')
    
    favs= Fav.query.filter_by(user_id=user_id).all()
    fav_list = []
    i = 0
    for result in favs:
        fav_details = Cocktails.query.filter_by(id=favs[i].cocktail_id)
        fav_list.append(fav_details) 
        i +=1
    return render_template('user-favs.html', cocktail_list=fav_list)

@app.route('/<int:user_id>/favorites/delete/<int:drink_id>', methods=["POST"])
def delete_cocktail(drink_id,user_id):
    fav = Fav.query.filter_by(cocktail_id=drink_id).first()
    db.session.delete(fav)
    db.session.commit()
    return redirect(f'/{user_id}/favorites')


# USER LOGIN AND REGISTER


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """User login handling"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session[CURR_USER_KEY] = user.id
            return redirect("/")
        else:
            form.username.errors = ["Invalid Username/Passwords"]

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """User register handling"""
    form = UserAddForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, first_name, last_name)
        db.session.add(user)
        db.session.commit()
        session[CURR_USER_KEY] = user.id
        flash("User Created", "success")
        return redirect("/")
    else:
        return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    session.pop(CURR_USER_KEY)
    flash("You have logged out successfully", "success")
    return redirect("/")


###########
