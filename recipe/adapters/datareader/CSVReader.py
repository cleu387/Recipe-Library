import csv
import ast
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.category import Category
from datetime import datetime
from dateutil import parser


class CSVReader:
    def __init__(self, filepath:str):
        self.__filepath = filepath

    def get_data(self):
        with open(self.__filepath, newline="") as csvfile:
            reader = csv.reader(csvfile)
            line_count = 0
            for row in reader:
                if line_count == 0:
                    line_count += 1
                else:
                    recipeId = int(row[0])
                    recipeName = row[1]
                    author = Author(int(row[2]), row[3])
                    cook_time = int(row[4])
                    preparation_time = int(row[5])
                    date = parser.parse(row[7])
                    description = row[8]
                    images = ast.literal_eval(row[9]) if row[9] else []
                    category = Category(row[10])
                    ingredient_quantity = row[11].split()
                    ingredients = ast.literal_eval(row[12]) if row[12] else []
                    # Nutrition class needs to be implemented first
                    nutrition = Nutrition(line_count, float(row[13]), float(row[14]), float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]), float(row[20]), float(row[21]))
                    servings = row[22]
                    recipe_yield = row[23]
                    instructions = ast.literal_eval(row[24]) if row[24] else []
                    recipe = Recipe(recipeId, recipeName, author, cook_time, preparation_time, date, description, images, category,
                                    ingredient_quantity, ingredients,None, nutrition, servings, recipe_yield, instructions)
                    yield recipe