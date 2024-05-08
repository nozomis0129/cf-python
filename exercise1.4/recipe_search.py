import pickle

def display_recipe(recipe):
  print('________________________________________')
  print('Name: ' + recipe['Name'])
  print('Cooking Time: ' + str(recipe['Cooking time']))
  print('Ingredients: ' + str(recipe['Ingredients']))
  print('Difficulty: ' + recipe['Difficulty'] )
  print('________________________________________')

def search_ingredient(data):
  print('All the available ingredients across recipes')
  indexed_ingredients = list(enumerate(data['all_ingredients'], 1))
  print(*indexed_ingredients, sep='\n')

  try:
    selection = int(input('Enter the number to select the ingredient: '))
    ingredient_searched = data['all_ingredients'][selection-1]
    print('The following recipes include ' + ingredient_searched + ': ')
  except:
    print('The ingredient number is not valid')
  else:
    for recipe in data['recipes_list']:
      for ingredient in recipe['Ingredients']:
        if ingredient == ingredient_searched:
          display_recipe(recipe)

filename = input('Enter the filename where recipes are stored: ')

try:
  recipe_file = open(filename, 'rb')
  data = pickle.load(recipe_file)
except FileNotFoundError:
  print('The file has\'t been found.')
else:
  search_ingredient(data)
finally:
  recipe_file.close()