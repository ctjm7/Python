import pickle

def display_recipe(recipe):
    print("Recipe: " + recipe['name'])
    print("Cooking Time (min): " + str(recipe['cooking_time']))
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("Difficulty level: " + recipe['difficulty'], end="\n\n")

def search_ingredient(data):
    ingredients_list = data['all_ingredients']
    for count, ingredient in enumerate(ingredients_list, 1):
        print(count, ingredient)
    try:
        ingredient_number = int(input('Pick a number from the list of ingredients: ')) - 1
        ingredient_searched = ingredients_list[ingredient_number]
        print("You have selected the ingredient: ", ingredient_searched)
    except:
        print('Unexpected input')
    else:
        for recipe in data['recipes_list']:
            if ingredient_searched in recipe['ingredients']:
                display_recipe(recipe)

# Opens file with recipe details
your_file = input("Enter the name of the file that contains your recipe: ")

try:
    recipe_filename = open(your_file, 'rb')
    data = pickle.load(recipe_filename)
except:
    print('File does not exist')
else:
    search_ingredient(data)
    recipe_filename.close()
