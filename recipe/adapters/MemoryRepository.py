from bisect import insort_left
from typing import List

from recipe.domainmodel.recipe import Recipe
from recipe.adapters.Repository import AbstractRepository
from pathlib import Path
from recipe.adapters.datareader.CSVReader import CSVReader

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__recipes = list()

    def add_recipe(self, recipe:Recipe):
        if isinstance(recipe, Recipe):
            insort_left(self.__recipes, recipe)

    def get_recipe(self) -> List[Recipe]:
        return self.__recipes

    def get_number_of_recipes(self) -> int:
        return len(self.__recipes)

    def get_all_recipe_id(self) -> list[int]:
        return [recipe.id for recipe in self.__recipes]

    def get_recipe_by_id(self, recipe_id:int) -> int:
        for recipe in self.__recipes:
            if recipe.id == recipe_id:
                return recipe
        raise ValueError(f"Recipe with id {recipe_id} not found")


def populate(repo: AbstractRepository):
    BASE_DIR = Path(__file__).resolve().parent
    filepath = BASE_DIR.parent / "adapters" / "datareader" / "data" / "recipes.csv"
    reader = CSVReader(str(filepath))
    data = reader.get_data()
    for recipe in data:
        repo.add_recipe(recipe)

