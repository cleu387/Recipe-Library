from flask import session

from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.favourite import Favourite

class NonExistentRecipe(Exception):
    pass

class UnknownUserException(Exception):
    pass



def get_favourites(username: str, repo: AbstractRepository) -> list[Favourite]:
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return repo.get_favourites(user)

def remove_favourite_recipe(recipe_id: int, username: str, repo: AbstractRepository):
    recipe = repo.get_recipe_by_id(recipe_id)
    if recipe is None:
        raise NonExistentRecipe

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    repo.remove_favourite(user, recipe)
