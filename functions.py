from model import db, connect_db, User, Cocktails, Cocktail_Ingredient, Fav, Ingredient


def add_cocktail(data):
    if  not  bool(Cocktails.query.filter(Cocktails.id == data["drinks"][0]['idDrink']).first()):
        new_cocktail = Cocktails(id=data["drinks"][0]['idDrink'], name = data["drinks"][0]['strDrink'],
                        img_url=data["drinks"][0]['strDrinkThumb'],
                        instructions = data["drinks"][0]['strInstructions'])
        db.session.add(new_cocktail)
        db.session.commit()

    for i in range (1,15):
        if data["drinks"][0][f'strIngredient{i}'] is not None:
            if  not bool(Ingredient.query.filter(Ingredient.ing_name == data["drinks"][0][f'strIngredient{i}']).first()):
                new_ingredient = Ingredient(ing_name=data["drinks"][0][f'strIngredient{i}'])
                db.session.add(new_ingredient)
                db.session.commit() 
            if not bool(Cocktail_Ingredient.query.filter(Cocktail_Ingredient.id== data["drinks"][0]['idDrink']).first()):
                ingredient= Ingredient.query.filter(Ingredient.ing_name == data["drinks"][0][f'strIngredient{i}']).first().id
                new_measurement = Cocktail_Ingredient(cocktail_id=data["drinks"][0]['idDrink'],
                                    ingredient_id =ingredient, 
                                    measurement=data["drinks"][0][f'strMeasure{i}'])
                db.session.add(new_measurement)
                db.session.commit()


def search_cocktail(data):
    for idx in len(data["drinks"]):
        if  not  bool(Cocktails.query.filter(Cocktails.id == data["drinks"][idx]['idDrink']).first()):
            new_cocktail = Cocktails(id=data["drinks"][idx]['idDrink'], name = data["drinks"][idx]['strDrink'],
                            img_url=data["drinks"][idx]['strDrinkThumb'],
                            instructions = data["drinks"][idx]['strInstructions'])
            db.session.add(new_cocktail)
            db.session.commit()

        for i in range (1,15):
            if data["drinks"][idx][f'strIngredient{i}'] is not None:
                if  not bool(Ingredient.query.filter(Ingredient.ing_name == data["drinks"][idx][f'strIngredient{i}']).first()):
                    new_ingredient = Ingredient(ing_name=data["drinks"][idx][f'strIngredient{i}'])
                    db.session.add(new_ingredient)
                    db.session.commit() 
                if not bool(Cocktail_Ingredient.query.filter(Cocktail_Ingredient.id== data["drinks"][idx]['idDrink']).first()):
                    ingredient= Ingredient.query.filter(Ingredient.ing_name == data["drinks"][idx][f'strIngredient{i}']).first().id
                    new_measurement = Cocktail_Ingredient(cocktail_id=data["drinks"][idx]['idDrink'],
                                        ingredient_id =ingredient, 
                                        measurement=data["drinks"][idx][f'strMeasure{i}'])
                    db.session.add(new_measurement)
                    db.session.commit()

