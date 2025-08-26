import abc
from typing import List
from recipe.domainmodel.recipe import Recipe

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