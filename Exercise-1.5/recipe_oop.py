class Recipe(object):
    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.cooking_time = 0
        self.ingredients = []
        self.difficulty = ''

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.difficulty = self.calculate_difficulty()

    def get_cooking_time(self):
        return self.cooking_time

    def add_ingredients(self, *ingredient):
        self.ingredients = ingredient
        self.difficulty = self.calculate_difficulty()
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = 'Intermediate'
        elif self.cooking_time >= 10 and len(self.ingredients) >=4:
            self.difficulty = 'Hard'
        return self.difficulty

    def get_difficulty(self):
        if self.difficulty == '':
            self.difficulty = self.calculate_difficulty()
            return self.difficulty
        else:
            return self.difficulty

    def search_ingredient(self, ingredient, ingredients):
        if ingredient in ingredients:
            return True
        else:
            return False

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in self.all_ingredients:
                self.all_ingredients.append(ingredient)

    def __str__(self):
        output = '\nRecipe: ' + str(self.name) + \
            '\nCooking Time (min): ' + str(self.cooking_time) + \
            '\nDifficulty: ' + str(self.difficulty) + \
            '\nIngredients: \n'
        for ingredient in self.ingredients:
            output += ingredient + '\n'
        return output

    def recipe_search(self, data, search_term):
        for recipe in data:
            if self.search_ingredient(search_term, recipe.ingredients):
                print(recipe.name)

recipes_list = []

tea = Recipe('Tea')
tea.add_ingredients('Tea Leaves', 'Sugar', 'Water')
tea.set_cooking_time(5)

coffee = Recipe('Coffee')
coffee.add_ingredients('Coffee Powder', 'Sugar', 'Water')
coffee.set_cooking_time(5)

cake = Recipe('Cake')
cake.add_ingredients('Sugar', 'Butter', 'Eggs', 'Vanilla Essence', 'Flour', 'Baking Powder', 'Milk')
cake.set_cooking_time(50)

banana_smoothie = Recipe('Banana Smoothie')
banana_smoothie.add_ingredients('Bananas', 'Milk', 'Peanut Butter', 'Sugar', 'Ice Cubes')
banana_smoothie.set_cooking_time(5)

recipes_list = [tea, coffee, cake, banana_smoothie]

for recipe in recipes_list:
    print(recipe)

print('-----------')
tea.recipe_search(recipes_list, 'Water')
print('-----------')
tea.recipe_search(recipes_list, 'Sugar')
print('-----------')
tea.recipe_search(recipes_list, 'Bananas')
