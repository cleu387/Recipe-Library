from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User
    from recipe.domainmodel.recipe import Recipe

class Favourite:
    def __init__(self, favourite_id: int, user: User, recipes: list[Recipe] = None):
        self.__id = favourite_id
        self.__user = user
        self.__recipes = recipes if recipes is not None else []

    def __repr__(self) -> str:
        return f"{self.user}: {self.recipes}"

    def __hash__(self) -> int :
        return hash(self.__id)

    def add_recipe(self, recipe: Recipe) -> None:
        if recipe not in self.__recipes:
            self.__recipes.append(recipe)

    def remove_recipe(self, recipe: Recipe) -> None:
        if recipe in self.__recipes:
            self.__recipes.remove(recipe)

    @property
    def user(self) -> User:
        return self.__user

    @property
    def recipes(self) -> list:
        return self.__recipes

    @property
    def id(self) -> int:
        return self.__id

