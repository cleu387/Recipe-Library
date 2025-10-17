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
    favourite = Favourite(user=user, recipe=recipe)
    repo.add_favourite(favourite)

def if_favourite_exists(recipe_id: int, user: User, repo: AbstractRepository):
    favourites = repo.get_favourites(user)
    return any(fav.recipe.id == recipe_id for fav in favourites)


def calculate_health_rating(nutrition):
    if nutrition is None:
        return None

    score = 5
    calories_per_meal = range(500,701)
    fat_per_meal = range(12,26)
    saturated_fat_per_meal = range(5,16)
    cholesterol_per_meal = 200
    sodium_per_meal = 900
    carbohydrates_per_meal = range(50,151)
    sugar_per_meal = 20
    fiber_per_meal = 5
    protein_per_meal = 15



    if nutrition.calories not in calories_per_meal:
        score -= 1
    if nutrition.fat not in fat_per_meal:
        score -= 0.5
    if nutrition.saturated_fat not in saturated_fat_per_meal:
        score -= 1
    if nutrition.cholesterol > cholesterol_per_meal:
        score -= 0.5
    if nutrition.sodium > sodium_per_meal:
        score -= 0.5
    if nutrition.carbohydrates not in carbohydrates_per_meal:
        score -= 0.5
    if nutrition.sugar > sugar_per_meal:
        score -= 1

    if nutrition.fiber > fiber_per_meal:
        score += 1
    if nutrition.protein > protein_per_meal:
        score += 1

    score = max(0, min(score, 5))

    return score
