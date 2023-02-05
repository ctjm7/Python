import mysql.connector

conn = mysql.connector.connect(host='localhost', user='cf-python', passwd='password')
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
	id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  ingredients VARCHAR(255),
	cooking_time INT,
  difficulty VARCHAR(20)
)''')

def calculate_difficulty(cooking_time, ingredients):
	if cooking_time < 10 and len(ingredients) < 4:
		difficulty = 'Easy'
	elif cooking_time < 10 and len(ingredients) >= 4:
		difficulty = 'Medium'
	elif cooking_time >= 10 and len(ingredients) < 4:
		difficulty = 'Intermediate'
	elif cooking_time >= 10 and len(ingredients) >=4:
		difficulty = 'Hard'
	return difficulty

# Main Menu function main_menu()
def main_menu(conn, cursor):
	choice = ''

	while(choice != 'quit'):
		print('\nMain Menu')
		print('===============================')
		print('Pick a choice:')
		print('  1. Create a new recipe')
		print('  2. Search for a recipe by ingredient')
		print('  3. Update an existing recipe')
		print('  4. Delete a recipe')
		print("  Type 'quit' to exit the program")
		choice = input('Your choice: ')

		if choice == '1':
			create_recipe(conn, cursor)
		elif choice == '2':
			search_recipe(conn, cursor)
		elif choice == '3':
			update_recipe(conn, cursor)
		elif choice == '4':
			delete_recipe(conn, cursor)

def create_recipe(conn, cursor):
    name = input('Enter the name of the recipe: ')
    cooking_time = int(input('Enter the cooking time in minutes: '))
    ingredients = input('Enter the ingredients separated by a comma: ')
    ingredients_list = ingredients.split(', ')
    difficulty = calculate_difficulty(cooking_time, ingredients_list)
    sql = 'INSERT INTO Recipes (name, cooking_time, ingredients, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, cooking_time, ingredients, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    print('Recipe has been saved')

# Search recipe
def search_recipe(conn, cursor):
	all_ingredients = []
	cursor.execute('SELECT ingredients FROM Recipes')
	results = cursor.fetchall()

	# Loops through the results to get all ingredients list
	for recipe_ingredients_list in results:
		for recipe_ingredients in recipe_ingredients_list:
			recipe_ingredients_split = recipe_ingredients.split(', ')
			all_ingredients.extend(recipe_ingredients_split)

	# Adds ingredients to all_ingredients
	all_ingredients = list(dict.fromkeys(all_ingredients))
	all_ingredients_list = list(enumerate(all_ingredients))

	print('\nAll Ingredients')
	print('----------------')

	for index, tup in enumerate(all_ingredients_list):
		print(str(tup[0] + 1) + '. ' + tup[1])

	search_index = int(input('\nEnter the corresponding number of the ingredient you want to select: ')) - 1
	search_ingredient = all_ingredients_list[search_index][1]

	cursor.execute('SELECT * FROM Recipes WHERE ingredients LIKE "%' + search_ingredient + '%"')
	recipes_with_search = cursor.fetchall()

	# Displays recipes that contains searched ingredient
	print('Recipes that contain ' + search_ingredient + ':')
	for row in recipes_with_search:
		print(row[1])

def update_recipe(conn, cursor):
	cursor.execute('SELECT * FROM Recipes')
	all_recipes = cursor.fetchall()

	print("\nAll Recipes")
	print('-----------')

	for row in all_recipes:
		print('\nID: ', row[0])
		print('Name: ', row[1])
		print('Cooking Time: ', row[3])
		print('Ingredients: ', row[2])
		print('Difficulty: ', row[4])

	recipe_id = str(input('\nEnter the id number of the recipe you would like to update: '))
	column_to_update = str(input('Type in name, cooking time, or ingredients to update: '))

	if column_to_update == 'name':
		new_name = str(input('Enter the new name for the recipe: '))
		cursor.execute('UPDATE Recipes SET name = %s WHERE id = %s', (new_name, recipe_id))
		print('Recipe name has been updated')
	elif column_to_update == 'cooking time':
		new_cooking_time = str(input('Enter the new cooking time: '))

		cursor.execute('UPDATE Recipes SET cooking_time = ' + new_cooking_time + ' WHERE id = ' + recipe_id)
		cursor.execute('SELECT * FROM Recipes WHERE id = ' + recipe_id)
		result_recipe = cursor.fetchall()

		cooking_time = int(new_cooking_time)
		ingredients = tuple(result_recipe[0][2].split(', '))
		updated_difficulty = calculate_difficulty(cooking_time, ingredients)

		cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (updated_difficulty,recipe_id))
		print('Recipe cooking time has been updated')
	elif column_to_update == 'ingredients':
		new_ingredients = str(input('Enter the ingredients separated by a comma: '))

		cursor.execute('UPDATE Recipes SET ingredients = %s WHERE id = %s', (new_ingredients,recipe_id))
		cursor.execute('SELECT * FROM Recipes WHERE id = ' + recipe_id)
		result_recipe = cursor.fetchall()

		cooking_time = int(result_recipe[0][3])
		ingredients = tuple(result_recipe[0][2].split(', '))
		updated_difficulty = calculate_difficulty(cooking_time, ingredients)

		cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (updated_difficulty,recipe_id))
		cursor.execute('UPDATE Recipes SET difficulty = %s WHERE id = %s', (updated_difficulty,recipe_id))
		print('Recipe ingredients have been updated')

	conn.commit()

def delete_recipe(conn, cursor):
	cursor.execute('SELECT id, name FROM Recipes')
	all_recipes = cursor.fetchall()

	print('All Recipes')
	print('-----------\n')
	for row in all_recipes:
		print(row[0], row[1])

	delete_recipe = str(input('Enter the number of the recipe you would like to delete: '))
	cursor.execute('DELETE FROM Recipes WHERE id = ' + delete_recipe)
	conn.commit()
	print('Recipe has been deleted')

main_menu(conn, cursor)
print('Goodbye')
