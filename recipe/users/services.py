from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe

class NonExistentRecipe(Exception):
    pass

class UnknownUserException(Exception):
    pass



def get_favourites(username: str, repo: AbstractRepository) -> list[Recipe]:
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    favourites = repo.get_favourites(user) #List of favourites
    if favourites:
        favourite = [repo.get_recipe_by_id(fav.recipe.id) for fav in favourites] #Convert to recipe objects
        return favourite
    else:
        return []

def remove_favourite_recipe(recipe_id: int, username: str, repo: AbstractRepository):
    recipe = repo.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise NonExistentRecipe

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    repo.remove_favourite(user, recipe)
