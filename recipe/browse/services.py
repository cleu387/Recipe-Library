from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.user import User
from recipe.domainmodel.favourite import Favourite

def get_number_of_recipes(repo, search_query=None, search_type="name"):
    return repo.get_recipe_count(search_query, search_type)

def get_recipe(repo, search_query=None, search_type="name", page=1, per_page=20):
    recipes = repo.get_recipes(page, per_page, search_query, search_type)
    recipe_dicts = []
    for recipe in recipes:
        recipe_dicts.append({
            "id": int(recipe.id),
            "name": recipe.name,
            "author": recipe.author.name,
            "category": recipe.category.name if recipe.category else "",
            "image": recipe.images[0] if recipe.images else "",
            "description": recipe.description,
            "rating": recipe.rating if recipe.rating is not None else None,

        })
    return recipe_dicts

def get_recipe_by_id(recipe_id: int, repo: AbstractRepository):
    return repo.get_recipe_by_id(recipe_id)

class NonExistentRecipe(Exception):
    pass

class UnknownUserException(Exception):
    pass

class FavouriteAlreadyExists(Exception):
    pass

def add_favourite_recipe(recipe_id: int, username: str, repo: AbstractRepository):
    recipe = repo.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise NonExistentRecipe

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    favourites = repo.get_favourites(user)

    for fav in favourites:
        if fav.user.id == user.id and fav.recipe.id == recipe.id:
            raise FavouriteAlreadyExists("The user has already favourite this recipe!")
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
