from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User
    from recipe.domainmodel.recipe import Recipe

class Favourite:
    def __init__(self, user: User, recipe: Recipe):
        self.__id = None
        self.__user = user
        self.__recipe = recipe

    def __repr__(self) -> str:
        return f"{self.user}: {self.recipe}"

    def __hash__(self) -> int :
        return hash(self.__id)

    def __eq__(self, other) -> bool:
        if isinstance(other, Favourite):
            return self.__id == other.__id and self.__user == other.__user and self.__recipe == other.__recipe
        return False

    @property
    def user(self) -> User:
        return self.__user

    @property
    def recipe(self) -> Recipe:
        return self.__recipe

    @property
    def id(self) -> int:
        return self.__id

