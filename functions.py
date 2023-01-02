from model import db, connect_db, User, Cocktails, Cocktail_Ingredient, Fav, Ingredient


def process_cocktail(cocktail):
    return {
        "id": cocktail["idDrink"],
        "name": cocktail["strDrink"],
        "image": cocktail["strDrinkThumb"],
        "instructions": cocktail["strInstructions"],
        "ingredients": [
            {
                "name": cocktail[f"strIngredient{i}"],
                "measurement": cocktail[f"strMeasure{i}"],
            }
            for i in range(1, 15)
        ],
    }


def add_cocktail(processed_cocktail):
    if not Cocktails.query.filter(Cocktails.id == processed_cocktail["id"]).first():
        new_cocktail = Cocktails(
            id=processed_cocktail["id"],
            name=processed_cocktail["name"],
            img_url=processed_cocktail["image"],
            instructions=processed_cocktail["instructions"],
        )
        db.session.add(new_cocktail)
        db.session.commit()

    for cocktails_ingredient in processed_cocktail["ingredients"]:
        db_ingredient_cocktail_to_add = []
        if cocktails_ingredient["name"] is not None:
            ingredient = cocktails_ingredient["name"]
            ingredient_measurement = cocktails_ingredient["measurement"]
            if not Ingredient.query.filter(Ingredient.ing_name == ingredient).first():
                new_ingredient = Ingredient(ing_name=ingredient)
                db.session.add(new_ingredient)
                db.session.commit()

                ingredient_id = (
                    Ingredient.query.filter(Ingredient.ing_name == ingredient)
                    .first()
                    .id
                )
                if not Cocktail_Ingredient.query.filter(
                    Cocktail_Ingredient.cocktail_id == processed_cocktail["id"],
                    Cocktail_Ingredient.ingredient_id == ingredient_id,
                ).first():

                    new_measurement = Cocktail_Ingredient(
                        cocktail_id=processed_cocktail["id"],
                        ingredient_id=ingredient_id,
                        measurement=ingredient_measurement,
                    )
                    db_ingredient_cocktail_to_add.append(new_measurement)
        db.session.add_all(db_ingredient_cocktail_to_add)
        db.session.commit()


def search_cocktail(search):
    search_result = []
    i = 0
    for cocktail in search:
        
        search_result_dict = {
        "id": search[i]["idDrink"],
        "name": search[i]["strDrink"],
        "image": search[i]["strDrinkThumb"],
        }
        i+=1
        search_result.append(search_result_dict)
    return search_result

