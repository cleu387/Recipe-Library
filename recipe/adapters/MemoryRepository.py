from bisect import insort_left
from typing import List

from recipe import Recipe
from recipe.adapters.Repository import AbstractRepository
from pathlib import Path
from recipe.adapters.datareader.CSVReader import CSVReader

class MemoryRepository(AbstractRepository):
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent
        filepath = BASE_DIR.parent / "adapters" / "datareader" / "data" / "recipes.csv"
        temp = CSVReader(str(filepath))
        self.__recipes = list(temp.get_data())

    def add_recipe(self, recipe:Recipe):
        self.__recipes.append(recipe)

    def get_recipe(self) -> List[Recipe]:
        return self.__recipes

    def get_number_of_recipes(self) -> int:
        return len(self.__recipes)


