from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from recipe.domainmodel.user import User
    from recipe.domainmodel.recipe import Recipe

from datetime import datetime

class Review:
    def __init__(self, user: User, recipe: Recipe, rating: int, review_text: str, created_date: datetime = None):
        self.__id = None
        self.__user = user
        self.__recipe = recipe
        self.__rating = rating
        self.__review_text = review_text
        self.__date = created_date if created_date else datetime.now()

    def __hash__(self) -> int:
        return hash(self.__id)

    def __repr__(self) -> str:
        return f"{self.user}: {self.recipe}: {self.rating} - {self.review_text}"


    @property
    def id(self) -> int:
        return self.__id

    @property
    def user(self) -> User:
        return self.__user

    @property
    def recipe(self) -> Recipe:
        return self.__recipe

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, rating: int) -> None:
        if rating < 0 or rating > 5:
            raise ValueError("Rating must be between 0 and 5")
        self.__rating = rating

    @property
    def review_text(self) -> str:
        return self.__review_text

    @review_text.setter
    def review_text(self, review_text: str) -> None:
        self.__review_text = review_text

    @property
    def date(self) -> datetime:
        return self.__date


