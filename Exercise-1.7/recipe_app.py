import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
engine = create_engine("mysql://cf-python:password@localhost/task_database")

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Creates columns and sets data types of integer and string
from sqlalchemy import Column
from sqlalchemy.types import Integer, String

# Creates tables of models defined
Base.metadata.create_all(engine)

# Creates an object from Session class to make changes to database
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Class that inherits Base and sets table
class Recipe(Base):
    __tablename__ = 'final_recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return '<Recipe ID: ' + str(self.id) + '-' + self.name + '-' + self.difficulty + '>'

    def __str__(self):
        output= '\nRecipe: ' + str(self.name) + \
            '\nCooking Time (min): ' + str(self.cooking_time) + \
            '\nDifficulty: ' + str(self.difficulty) + \
            '\nIngredients: ' + str(self.ingredients)
        return output

    # Calculates difficulty level using cooking_time and ingredients
    def calculate_difficulty(self, cooking_time, ingredients):
        if cooking_time < 10 and len(ingredients) < 4:
            self.difficulty = 'Easy'
        elif cooking_time < 10 and len(ingredients) >= 4:
            self.difficulty = 'Medium'
        elif cooking_time >= 10 and len(ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif cooking_time >= 10 and len(ingredients) >=4:
            self.difficulty = 'Hard'
        return self.difficulty

    # Retrieves the ingredeints from Recipe returns it as a list
    def return_ingredients_as_list(self):
        recipes_list = session.query(Recipe).all()
        for recipe in recipes_list:
            ingredients_list = recipe.ingredients.split(', ')
            return ingredients_list

# Adds a recipe to the database and calculates difficulty
def create_recipe():
    name = input('Enter the name of the recipe: ')
    while len(name) > 50:
        name = input('Please enter a name less than 50 characters: ')

    cooking_time = input('Enter the cooking time in minutes: ')
    while cooking_time.isnumeric() == True:
        cooking_time = int(cooking_time)
    else:
        cooking_time = input('Please only enter a numerical value for cooking time: ')

    ingredients = []
    number_ingredients = input('Enter the number of ingredients you will be adding: ')
    while number_ingredients.isnumeric() == False:
        number_ingredients = int(input('Please enter a numerical value for the number of ingredients: '))
    for i in range (int(number_ingredients)):
        ingredient = input('Enter an ingredient: ')
        ingredients.append(ingredient)
    ingredients_str = ', '.join(ingredients)

    difficulty = Recipe.calculate_difficulty(cooking_time, ingredients)

    recipe_entry = Recipe(
         name = name,
         cooking_time = cooking_time,
         ingredients = ingredients_str,
         difficulty = difficulty
	)
    session.add(recipe_entry)
    session.commit()
    print('Recipe has been saved')

# Lists all recipes that are saved to the database
def view_all_recipes():
    recipes_list = session.query(Recipe).all()
    if len(recipes_list) == 0:
        print('There are no recipes saved')
        return None
    else:
    	for recipe in recipes_list:
        	print(recipe)

# Retrieves recipes that contain ingredients that are input by user
def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("There are no recipes saved")
        return None
    else:
        results = session.query(Recipe.ingredients).all()
        all_ingredients = []
        for recipe_ingredients_list in results:
            for recipe_ingredients in recipe_ingredients_list:
                recipe_ingredients_split = recipe_ingredients.split(', ')
                all_ingredients.extend(recipe_ingredients_split)
        all_ingredients = list(dict.fromkeys(all_ingredients))
        all_ingredients_list = list(enumerate(all_ingredients))

        print('\nAll Ingredients')
        print('----------------')
        for index, tup in enumerate(all_ingredients_list):
            print(str(tup[0] + 1) + '. ' + tup[1])

        search_index = input('\nEnter the corresponding number of the ingredient(s) you want to select separated by a space: ')
        search_index_list = search_index.split(' ')

        ingredients_searched_list = []
        for n in search_index_list:
             ingredient_index = int(n) - 1
             ingredient_searched = all_ingredients_list[ingredient_index][1]
             ingredients_searched_list.append(ingredient_searched)

        conditions = []
        for ingredient in ingredients_searched_list:
            like_term = '%' + ingredient + '%'
            conditions.append(Recipe.ingredients.like(like_term))
        results = session.query(Recipe).filter(*conditions).all()
        for result in results:
            print(result.name)

# Deletes one recipe by selecting id from all recipes list
def delete_recipe():
    if session.query(Recipe).count() == 0:
        print('There are no recipes saved')
        return None
    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        for recipe in results:
            print('Recipe ID: ' + str(recipe.id) + ' -' + recipe.name)
        recipe_id = int(input('Enter the ID of the recipe you want to delete: '))
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == recipe_id).one()
        session.delete(recipe_to_delete)
        session.commit()
        print('The recipe ' + recipe.name + ' has been deleted')

# Edits a selected recipe
def edit_recipe():
    if session.query(Recipe).count() == 0:
        print('There are no recipes saved')
        return None
    else:
        results = session.query(Recipe).with_entities(Recipe.id, Recipe.name).all()
        print('-'*9)
        for result in results:
            print('Recipe ID: ' + str(result[0]) + ' -' + result[1])
        recipe_id = int(input('Enter the recipe id you want to edit: '))
        for result in results:
            if result[0] != recipe_id:
                 return None
            else:
                recipe_to_edit = session.query(Recipe).filter(Recipe.id == recipe_id).one()
                print('\nRecipe to edit')
                print('--------------')
                print(recipe_to_edit)

                choice = input('Enter the number of the attribute you want to update\n1. name, 2. ingredients, 3. cooking time: ')
                if choice.isnumeric() == True:
                    if choice == '1':
                        new_name = input('Enter the new name of the recipe: ')
                        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.name: new_name})
                        session.commit()
                        print('Recipe has been updated')
                    elif choice == '2':
                        new_ingredients = input('Enter the new ingredients for the recipe separated by a comma: ')
                        new_ingredients_list = new_ingredients.split(', ')
                        new_difficulty = Recipe.calculate_difficulty(recipe_to_edit.cooking_time, new_ingredients_list)
                        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.ingredients: new_ingredients, Recipe.difficulty: new_difficulty})
                        session.commit()
                        print('Recipe has been updated')
                    elif choice == '3':
                        new_cooking_time = int(input('Enter the new cooking time in minutes: '))
                        new_difficulty = Recipe.calculate_difficulty(new_cooking_time, recipe_to_edit.ingredients.split(', '))
                        session.query(Recipe).filter(Recipe.id == recipe_id).update({Recipe.cooking_time: new_cooking_time, Recipe.difficulty: new_difficulty})
                        session.commit()
                        print('Recipe has been updated')
                else:
                    print('You need to enter a number from 1 to 3')

# Main Menu function main_menu()
def main_menu():
	choice = ''

	while(choice != 'quit'):
		print('\nMain Menu')
		print('===============================')
		print('Pick a choice:')
		print('  1. Create a new recipe')
		print('  2. Search for a recipe by ingredient')
		print('  3. Update an existing recipe')
		print('  4. Delete a recipe')
		print('  5. View all recipes')
		print("  Type 'quit' to exit the program")
		choice = input('Your choice: ')

		if choice == '1':
			create_recipe()
		elif choice == '2':
			search_by_ingredients()
		elif choice == '3':
			edit_recipe()
		elif choice == '4':
			delete_recipe()
		elif choice == '5':
			view_all_recipes()


main_menu()
print('Goodbye')
session.close()
