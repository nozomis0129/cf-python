recipes_list = []
ingredients_list = []

def take_recipe ():
  name = input("Recipe name: ")
  cooking_time = int(input("Cooking time in minutes: "))
  ingredients = input("Ingredients(separate by a comma): ").split(", ")
  recipe = {
    'name': name,
    'cooking_time': cooking_time,
    'ingredients': ingredients
  }
  return recipe

n = int(input("How many recipes would you like to add?: "))

for i in range(n):
  recipe = take_recipe()

  for ingredient in recipe['ingredients']:
    if not ingredient in ingredients_list:
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

for recipe in recipes_list:
  if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
    recipe['difficulty'] = 'easy'
  elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
    recipe['difficulty'] = 'medium'
  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
    recipe['difficulty'] = 'intermedate'
  elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >= 4:
    recipe['difficulty'] = 'hard'

for recipe in recipes_list:
  print('Recipe: ', recipe['name'])
  print('Cooking Time (min): ', recipe['cooking_time'])
  print('Ingredients:')
  for ingredient in recipe['ingredients']:
    print(ingredient)
  print('Difficulty level: ', recipe['difficulty'])

def print_ingredients():
  ingredients_list.sort()
  print('Ingredients Available Across All Recipes')
  print('________________________________________')
  for ingredient in ingredients_list:
    print(ingredient)

print_ingredients()