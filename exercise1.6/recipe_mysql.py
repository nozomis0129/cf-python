import mysql.connector

conn = mysql.connector.connect(
  host='localhost',
  user='cf-python',
  passwd='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
  id            INT AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(50),
  ingredients   VARCHAR(250),
  cooking_time  INT,
  difficulty    VARCHAR(20)
)''')

def main_menu(conn, cursor):
  choice = ''
  while(choice != 'quit'):
    print()
    print('\nMain Menu')
    print('=====================================================')
    print(' Pick a choice:')
    print('        1. Create a new recipe')
    print('        2. Search for a specific recipe by ingredient')
    print('        3. Update a recipe')
    print('        4. Delete a recipe')
    print('        5. View all recipes')
    print('\n Type "quit" to exit the program')
    choice = input('\nYour choice: ')
    print('\n===================================================')

    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)
    elif choice == '5':
      view_all_recipes(conn, cursor)


def create_recipe(conn, cursor):
  recipe_ingredients = []
  name = str(input('\nEnter the name of the recipe: '))
  cooking_time = int(input('Cooking time in minutes: '))
  ingredient = input('Enter ingredients: ')
  recipe_ingredients.append(ingredient)
  difficulty = calculate_difficulty(cooking_time, recipe_ingredients)

  # To store ingredients into a comma separated string
  ingredients_data = ','.join(recipe_ingredients)

  sql = 'INSERT INTO Recipes (name, cooking_time, ingredients, difficulty) VALUES (%s, %s, %s, %s)'
  val = (name, cooking_time, ingredients_data, difficulty)

  cursor.execute(sql, val)
  conn.commit()
  print('Recipe saved into the database.')


def calculate_difficulty(cooking_time, recipe_ingredients):
    if cooking_time < 10 and len(recipe_ingredients) < 4:
      difficulty = 'Easy'
    elif cooking_time < 10 and len(recipe_ingredients) >= 4:
      difficulty = 'Medium'
    elif cooking_time >= 10 and len(recipe_ingredients) < 4:
      difficulty = 'Intermediate'
    elif cooking_time >= 10 and len(recipe_ingredients) >= 4:
      difficulty = 'Hard'
    else:
      print('Something bad happened. Please try again.')

    print('Difficulty level: ', difficulty)
    return difficulty


def search_recipe(conn, cursor):
  all_ingredients = []
  cursor.execute('SELECT ingredients FROM Recipes')
  results = cursor.fetchall()
  for ingredients_list in results:
    for recipe_ingredients in ingredients_list:
      ingredients_split = recipe_ingredients.split(', ')
      all_ingredients.extend(ingredients_split)

  # Create a dictionary with values
  all_ingredients = list(dict.fromkeys(all_ingredients))
  # Number each ingredients
  all_ingredients_list = list(enumerate(all_ingredients))

  print('\nAll ingredients list:')
  print('------------------------')

  # Allow user to pick a number corresponding to the ingredients
  for index, tup in enumerate(all_ingredients_list):
    print(str(tup[0]+1) + '. ' + tup[1])

  try:
    ingredient_searched_num = input(
      '\nEnter the number corresponding to the ingredient you want to pick from the list: ')
    ingredient_searched_index = int(ingredient_searched_num) - 1
    ingredient_searched = all_ingredients_list[ingredient_searched_index][1]

    print('\nIngredient you selected: ', ingredient_searched)

  except:
    print('Unexpected error occurred. Please try again.')

  else:
    print('\nThe recipe(s) include(s) the selected ingredient: ')
    print('-------------------------------------------------')

    cursor.execute('SELECT * FROM Recipes WHERE ingredients LIKE %s', 
    ('%' + ingredient_searched + '%', ))

    result_recipes = cursor.fetchall()
    for row in result_recipes:
      print('\nID: ', row[0])
      print('Name: ', row[1])
      print('Cooking time: ', row[3])
      print('Ingredients: ', row[2])
      print('Difficulty: ', row[4])


def update_recipe(conn, cursor):
  # Display all recipes
  view_all_recipes(conn, cursor)

  id_for_update = int(
    input('\nEnter the ID of the recipe you want to update: '))
  column_for_update = str(
    input('\nEnter the data you want to update.(select "name", "cooking_time", or "ingredients"): '))
  updated_value = (input('\nEnter new value: '))
  print('What you entered: ', updated_value)

  if column_for_update == 'name':
    cursor.execute('UPDATE Recipes SET name = %s WHERE id = %s', (updated_value, id_for_update))
    print('Recipe name has been updated.')

  elif column_for_update == 'cooking_time':
    cursor.execute('UPDATE Recipes SET cooking_time = %s WHERE id = %s', (updated_value, id_for_update))
    cursor.execute('SELECT * FROM Recipes WHERE id = %s', (id_for_update, ))
    result_recipe_for_update = cursor.fetchall()

    name = result_recipe_for_update[0][1]
    cooking_time = result_recipe_for_update[0][3]
    ingredients = tuple(result_recipe_for_update[0][2].split(','))

    updated_difficulty = calculate_difficulty(cooking_time, ingredients)
    print('Updated difficulty: ', updated_difficulty)
    cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (updated_difficulty, id_for_update))
    print('Modification done')

  elif column_for_update == 'ingredients':
    cursor.execute('UPDATE Recipes SET ingredients = %s WHERE id = %s', (updated_value, id_for_update))
    cursor.execute('SELECT * FROM Recipes WHERE id = %s', (id_for_update, ))
    result_recipe_for_update = cursor.fetchall()

    name = result_recipe_for_update[0][1]
    cooking_time = result_recipe_for_update[0][3]
    recipe_ingredients = tuple(result_recipe_for_update[0][2].split(','))
    difficulty = result_recipe_for_update[0][4]

    updated_difficulty = calculate_difficulty(cooking_time, recipe_ingredients)
    print('Updated difficulty: ', updated_difficulty)
    cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (updated_difficulty, id_for_update))
    print('Modification done')

  conn.commit()


def delete_recipe(conn, cursor):
   # Display all recipes
  view_all_recipes(conn, cursor)

  id_for_delete = input('\nEnter the ID of the recipe you want to delete: ')
  cursor.execute('DELETE FROM Recipes WHERE id = (%s)', (id_for_delete, ))

  conn.commit()
  print('Recipe has been deleted.')


def view_all_recipes(conn, cursor):
  print('\nAll recipes:')
  print('-----------------------------------------')

  cursor.execute('SELECT * FROM Recipes')
  results = cursor.fetchall()

  for row in results:
    print('\nID: ', row[0])
    print('Name: ', row[1])
    print('Cooking time: ', row[3])
    print('Ingredients: ', row[2])
    print('Difficulty: ', row[4])

main_menu(conn, cursor)