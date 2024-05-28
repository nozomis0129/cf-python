from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()

engine = create_engine("mysql://cf-python:password@localhost/task_database")

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Quick representation of the recipe
    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"

    # Details about the recipe
    def __str__(self):
        output = "\n--------------------------------------------------" + \
            "\nRecipe name: " + str(self.name) + \
            "\nIngredients: " + str(self.ingredients) + \
            "\nCooking time: " + str(self.cooking_time) + " min" + \
            "\nDifficulty: " + str(self.difficulty)
        return output

# Create all defined table in the database
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()


def calculate_difficulty(cooking_time, recipe_ingredients):
    if cooking_time < 10 and len(recipe_ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(recipe_ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(recipe_ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(recipe_ingredients) >= 4:
        difficulty = "Hard"
    else:
        print("Something bad happened. Please try again.")

    print("Difficulty level: ", difficulty)
    return difficulty


def return_ingredients_as_list():
    recipe_list = session.query(Recipe).all()
    for recipe in recipe_list:
        print("Recipe: ", recipe)
        print("Ingredients: ", recipe.ingredients)
        recipe_ingredients_list = recipe_ingredients.split(",")
        print(recipe_ingredients_list)


# Main 5 functions come down below
# 1. Create recipes
def create_recipe():
    recipe_ingredients = []

    correct_input_name = False
    while correct_input_name == False:

        name = input("\nEnter the recipe name: ")
        if 0 < len(name) <= 50:
            correct_input_name = True

            correct_input_cooking_time = False
            while correct_input_cooking_time == False:
                cooking_time = input("Enter the cooking time in minutes: ")
                if cooking_time.isnumeric() == True:
                    correct_input_cooking_time = True
                else:
                    print("Please enter a positive number.")
        else:
            print("Please enter a valid recipe name(1-50 characters).")
        correct_input_number = False
        while correct_input_number == False:
            num_of_ingredients = input("How many ingredients would you like to enter?: ")
            if num_of_ingredients.isnumeric() == True:
                correct_input_number = True

                for _ in range(int(num_of_ingredients)):
                    ingredient = input("Input one ingredient and hit enter: ")
                    recipe_ingredients.append(ingredient)

            else:
                correct_input_number = False
                print("Please enter a positive number.")

    recipe_ingredients_str = ", ".join(recipe_ingredients)
    print(recipe_ingredients_str)
    difficulty = calculate_difficulty(int(cooking_time), recipe_ingredients)

    recipe_entry = Recipe(
        name=name,
        ingredients=recipe_ingredients_str,
        cooking_time=int(cooking_time),
        difficulty=difficulty
    )

    print(recipe_entry)

    # Add this new recipe to the database
    session.add(recipe_entry)
    try:
        session.commit()
        print("Recipe successfully added to the database!")
    except Exception as error:
        # Rollback in case of error during commit
        session.rollback()
        print("Error occurred: ", error)


# 2. View all recipes
def view_all_recipes():
    all_recipes = []
    all_recipes = session.query(Recipe).all()

    if len(all_recipes) == 0:
        print("\nTere are no recipes in the database.")
        print("Please create new recipe.")
        return None

    else:
        print("=========================================")
        print("           View All Recipes              ")
        print("=========================================")

        for recipe in all_recipes:
            print(recipe)


# 3. Search the recipe by ingredient
def search_by_ingredients():
    # Check if any recipes exist on the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        print("Please create a recipe first.")
        return None

    else:
        results = session.query(Recipe.ingredients).all()

        all_ingredients = []

        for recipe_ingredients_list in results:
            for recipe_ingredients in recipe_ingredients_list:
                recipe_ingredient_split = recipe_ingredients.split(", ")
                all_ingredients.extend(recipe_ingredient_split)

        # Create a dictionary with values
        all_ingredients = list(dict.fromkeys(all_ingredients))
        # Number each ingredients
        all_ingredients_list = list(enumerate(all_ingredients))

        print("=========================================")
        print("         All ingredients list            ")
        print("=========================================")

        # Allow user to pick a number corresponding to the ingredients
        for index, tup in enumerate(all_ingredients_list):
            print(str(tup[0] + 1) + ". " + tup[1])

        try:
            ingredient_searched_num = input(
                "\nEnter the number corresponding to the ingredient you want to pick from the list: "
            )

            ingredient_num_list_searched = ingredient_searched_num.split(" ")

            ingredient_searched_list = []
            for ingredient_searched_num in ingredient_num_list_searched:
                # Because ID starts from 0
                ingredient_searched_index = int(ingredient_searched_num) - 1
                # So that I can get only ingredient not index number
                ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

                ingredient_searched_list.append(ingredient_searched)

            print("\nYou selected the ingredient: ", ingredient_searched_list)

            conditions = []
            for ingredient in ingredient_searched_list:
                like_term = "%" + ingredient + "%"
                condition = Recipe.ingredients.like(like_term)
                conditions.append(condition)
          
            searched_recipes = session.query(Recipe).filter(*conditions).all()
          
        except:
            print("Unexpected error occurred. Please select the number again.")

        else:
            print("\nSearched recipe(s): ")
            for recipe in searched_recipes:
                print(recipe)


# 4. Edit recipe
def edit_recipe():
    # Check if any recipes exist on the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        print("Please create a recipe first.")
        return None

    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        print("List of available recipes:")
        for recipe in results:
            print("\nID: ", recipe[0])
            print("Recipe name: ", recipe[1])

        id_for_edit = int(input("\nEnter the recipe ID you want to edit: "))

        recipes_id_tup_list = session.query(Recipe).with_entities(Recipe.id).all()
        recipes_id_list = []

        for recipe_tup in recipes_id_tup_list:
            recipes_id_list.append(recipe_tup[0])

        if id_for_edit not in recipes_id_list:
            print("No such ID in the database. Please try again.")
        else:
            recipe_to_edit = session.query(Recipe).filter(Recipe.id == id_for_edit).one()
            
            print("\n** You are about to edit this recipe. **")
            print(recipe_to_edit)
            print("\n--------------------------------------------------")
            print("1. Recipe name, 2. Cooking time, 3. Ingredients")

            column_for_update = int(
                input("\nEnter the number you want to update among 1 ~ 3. : ")
            )
            updated_value = input("\nEnter the new value for the recipe: ")

            if column_for_update == 1:
                session.query(Recipe).filter(Recipe.id == id_for_edit).update(
                    {Recipe.name: updated_value}
                )
                session.commit()
                print("The recipe name has been updated.")

            elif column_for_update == 2:
                session.query(Recipe).filter(Recipe.id == id_for_edit).update(
                    {Recipe.cooking_time: updated_value}
                )
                session.commit()
                print("The cooking time has been updated.")

            elif column_for_update == 3:
                session.query(Recipe).filter(Recipe.id == id_for_edit).update(
                    {Recipe.ingredients: updated_value}
                )
                session.commit()
                print("The ingredients have been updated.")

            else:
                print("Wrong input, please try again.")

            updated_difficulty = calculate_difficulty(
                recipe_to_edit.cooking_time, recipe_to_edit.ingredients
            )
            print("updated_difficulty: ", updated_difficulty)
            recipe_to_edit.difficulty = updated_difficulty
            session.commit()
            print("Modification done.")


# 5. Delete recipe
def delete_recipe():
    # Check if any recipes exist on the database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database.")
        print("Please create a recipe first.")
        return None

    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        print("List of available recipes:")
        for recipe in results:
            print("\nID: ", recipe[0])
            print("Recipe name: ", recipe[1])

        id_for_deletion = input("\nEnter the Recipe ID you want to delete: ")

        recipe_being_deleted = (
            session.query(Recipe).filter(Recipe.id == id_for_deletion).one()
        )

        print("\n** You are about to delete this recipe. **")
        print(recipe_being_deleted)
        deletion_confirmed = input("\nAre you sure to delete the recipe? (y/n): ")
        if deletion_confirmed == "y":
            session.delete(recipe_being_deleted)
            session.commit()
            print("The Recipe has been deleted from the database.")
        else:
            return None


# Main menu
def main_menu():
    choice = ""
    while choice != "quit":
        print()
        print("\nMain Menu")
        print("=====================================================")
        print(" Pick a choice:")
        print("      1. Create a new recipe")
        print("      2. Search for a specific recipe by ingredient")
        print("      3. Update a recipe")
        print("      4. Delete a recipe")
        print("      5. View all recipes")
        print('\n Type "quit" to exit the program')
        choice = input("\nYour choice: ")
        print("\n=====================================================")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            search_by_ingredients()
        elif choice == "3":
            edit_recipe()
        elif choice == "4":
            delete_recipe()
        elif choice == "5":
            view_all_recipes()
        else:
            if choice == "quit":
                print("Bye!\n")
            else:
                print("Worng entry. Please try again.")


main_menu()
session.close()
