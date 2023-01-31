import pickle

recipe = {
  'Ingredient Name': 'Tea',
  'Ingredients': ['Tea Leaves', 'Water', 'Sugar'],
  'Cooking time' : 5,
  'Difficulty': 'Easy'
}

recipe_data = open('recipe_binary.bin', 'wb')
pickle.dump(recipe, recipe_data)
recipe_data.close()

with open('recipe_binary.bin', 'rb') as recipe_data:
    recipe = pickle.load(recipe_data)

print('Recipe')
print('------')
print('Ingredient Name: ', recipe[ 'Ingredient Name'])
print('Ingredients: ', recipe[ 'Ingredients'])
print('Cooking Time: ', recipe[ 'Cooking time'])
print('Difficulty: ', recipe[ 'Difficulty'])
