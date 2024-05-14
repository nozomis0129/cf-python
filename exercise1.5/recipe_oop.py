class Recipe:
  # Store all the ingredients of all recipes
  all_ingredients = set()

  # Initialization method with recipe name and cooking time
  def __init__(self, name, cooking_time):
    self.name = name
    self.ingredients = []
    self.cooking_time = cooking_time # Cooking time in minutes
    self.difficulty = None # Difficulty will be calculated in later function

  def get_name(self):
    return self.name

  def set_name(self, name):
    self.name = name

  def get_cooking_time(self):
    return self.cooking_time

  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time

  # Add ingredients to the recipe
  def add_ingredients(self, *args):
    for ingredient in args:
      self.ingredients.append(ingredient)
    self.update_all_ingredients() # Update class variable with new ingredients

  # Update the class variable all_ingredients with unique ingredients
  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      Recipe.all_ingredients.add(ingredient)

  def get_ingredients(self):
    return self.ingredients

  def calculate_difficulty(self):
    if self.cooking_time < 10 and len(self.ingredients) < 4:
      self.difficulty = 'Easy'
    elif self.cooking_time < 10 and len(self.ingredients) >= 4:
      self.difficulty = 'Medium'
    elif self.cooking_time >= 10 and len(self.ingredients) < 4:
      self.difficulty = 'Intermediate'
    else:
      self.difficulty = 'Hard'
  
  # Get difficulty if it's not done yet
  def get_difficulty(self):
    if self.difficulty is None:
      self.calculate_difficulty()
    return self.difficulty

  def search_ingredient(self, ingredient):
    return ingredient in self.ingredients

  # String representation of the recipes
  def __str__(self):
    self.calculate_difficulty()
    return f"\nRecipe name: {self.name} \
      \nCooking time: {self.cooking_time} minutes \
      \nIngredients: {','.join(self.ingredients)} \
      \nDifficulty: {self.difficulty}"

# Function to search recipe based on specific ingredient
def recipe_search(data, search_term):
  for recipe in data:
    if recipe.search_ingredient(search_term):
      print(recipe)

# Main code

tea = Recipe('Tea', 5)
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
print(tea)

coffee = Recipe('Coffee', 5)
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
print(coffee)

cake = Recipe('Cake', 50)
cake.add_ingredients('Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
print(cake)

banana_smoothie = Recipe('Banana Smoothie', 5)
banana_smoothie.add_ingredients('Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

print('---------------------------')
print('\nRecipes including Water:')
recipe_search(recipes_list, 'Water')

print('---------------------------')
print('\nRecipes including Sugar:')
recipe_search(recipes_list, 'Sugar')

print('---------------------------')
print('\nRecipes including Bananas:')
recipe_search(recipes_list, 'Bananas')