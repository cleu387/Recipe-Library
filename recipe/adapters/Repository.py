import abc
from typing import List
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User
from recipe.domainmodel.favourite import Favourite

repo_instance = None

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_recipe(self, recipe:Recipe):
        """ Add recipe to recipe repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe(self) -> List[Recipe]:
        """ Returns the list of recipes"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_recipes(self) -> int:
        """ Returns the number of recipes """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_recipe_id(self) -> list[int]:
        """ Returns all recipes' id """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id:int):
        """ Returns the recipe by id """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_favourite(self, user: User, recipe: Recipe) -> Favourite:
        """" Adds a Favourite Recipe to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite(self, user: User, recipe: Recipe):
        """" Removes a Favourite Recipe to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_favourites(self, user: User) -> List[Recipe]:
        """" Gets a list of Favourite Recipes to the repository. """
        raise NotImplementedError
