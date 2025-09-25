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
            "id": int(recipe.id),
            "name": recipe.name,
            "author": recipe.author.name,
            "category": recipe.category.name if recipe.category else "",
            "image": recipe.images[0] if recipe.images else "",
            "description": recipe.description,
            "rating": recipe.rating if recipe.rating is not None else None,

        }
        recipe_dicts.append(recipe_dict)
    return recipe_dicts

def get_recipe_by_id(recipe_id: int, repo: AbstractRepository):
    return repo.get_recipe_by_id(recipe_id)

class NonExistentRecipe(Exception):
    pass

class UnknownUserException(Exception):
    pass

def add_favourite_recipe(recipe_id: int, username: str, repo: AbstractRepository):
    recipe = repo.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise NonExistentRecipe

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    repo.add_favourite(user, recipe)


def calculate_health_rating(nutrition):
    if nutrition is None:
        return None

    score = 5

    if nutrition.calories > 500:
        score -= 1
    if nutrition.fat > 20:
        score -= 1
    if nutrition.saturated_fat > 5:
        score -= 1
    if nutrition.cholesterol > 100:
        score -= 1
    if nutrition.sodium > 600:
        score -= 1
    if nutrition.carbohydrates > 60:
        score -= 1
    if nutrition.sugar > 25:
        score -= 1

    if nutrition.fiber >= 5:
        score += 1
    if nutrition.protein >= 10:
        score += 1

    if score > 5:
        score = 5
    if score < 0:
        score = 0

    return score
