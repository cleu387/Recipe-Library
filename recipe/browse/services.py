from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition

def get_number_of_recipes(repo: AbstractRepository):
    return repo.get_number_of_recipes()

def get_recipe(repo: AbstractRepository):
    recipes = repo.get_recipe()
    recipe_dicts = []
    for recipe in recipes:
        recipe_dict = {
            "id": recipe.id,
            "name": recipe.name,
            "author": recipe.author.name,
        }
        recipe_dicts.append(recipe_dict)
    return recipe_dicts

def get_recipe_by_id(recipe_id: int, repo: AbstractRepository):
    recipes = repo.get_recipe()
    for recipe in recipes:
        if recipe.id == recipe_id:
            return recipe
    return None