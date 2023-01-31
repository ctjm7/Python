import pickle

# Determine recipe difficulty based on input values
def calc_difficulty(recipe):
    if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) >=4:
        recipe['difficulty'] = 'Hard'
    return recipe['difficulty']

# Acquire recipe information and call calc_difficulty
def take_recipe ():
    name = str(input("Enter the recipe name: "))
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the list of ingredients: ").split(', ')
    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    recipe['difficulty'] = calc_difficulty(recipe)
    return recipe


recipes_list = []
all_ingredients = []

# Opens file with recipe details
your_file = input("Enter the name of the file that contains your recipe: ")
try:
    recipe_filename = open(your_file, 'rb')
    data = pickle.load(recipe_filename)

except FileNotFoundError:
    print('File does not exist')
    data = {'recipes_list': [], 'all_ingredients': []}

except:
    print('An unexpected error occured')
    data = {'recipes_list': [], 'all_ingredients': []}

else:
    recipe_filename.close()

finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

# Asks user for number of recipes they want to enter
n = int(input("Please specify how many recipes would you like to enter: "))

# Collects recipe information from the user
for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

print("*****")

# Prints each recipe details
for recipe in recipes_list:
    print("Recipe: " + recipe['name'])
    print("Cooking Time (min): " + str(recipe['cooking_time']))
    print("Ingredients:")
    for ingredient in recipe['ingredients']:
        print(ingredient)
    print("Difficulty level: " + recipe['difficulty'], end="\n\n")

# Prints all ingredients from all recipes
print("Ingredients Available Across All Recipes")
print("----------------------------------------")
all_ingredients.sort()
for ingredient in all_ingredients:
    print(ingredient)

# Creates a dictionary containing recipes and ingredients
data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

print('Recipes list and ingredients from data', data)

entered_filename = str(input('Enter a name for your file: '))
new_file = open(entered_filename, 'wb')
pickle.dump(data, new_file)
new_file.close()
