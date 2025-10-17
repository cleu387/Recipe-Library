from datetime import datetime
from bisect import insort_left
from typing import List

from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__authors = list()
        self.__categories = list()
        self.__recipes = list()
        self.__reviews = dict()
        self.__users = list()
        self.__tags = list()
        self.__favourite_id_counter = 1
        self.__favourites = list()
        self._next_user_id = 1
        self._next_category_id = 1
        self._next_tag_id = 1

    #region Authors_data
    def add_author(self, author: Author):
        self.__authors.append(author)

    def get_authors(self) -> list[Author]:
        return self.__authors

    def get_number_of_authors(self) -> int:
        return len(self.__authors)

    def add_multiple_authors(self, authors: List[Author]):
        for author in authors:
            self.add_author(author)

    #endregion

    #region Category_data
    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance")
        if category.id is None:
            category._Category__id = self._next_category_id
            self._next_category_id += 1
        self.__categories.append(category)

    def get_categories(self) -> List[Category]:
        """
        Returns a list of all Categories in the repository.
        """
        return self.__categories

    def get_number_of_categories(self) -> int:
        return len(self.__categories)

    def add_multiple_categories(self, categories: List[Category]):
        for category in categories:
            self.add_category(category)

    #endregion

    #region Recipe_data
    def add_recipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        self.__recipes.append(recipe)

    def add_multiple_recipes(self, recipes: List[Recipe]):
        """
        Adds multiple Recipes to the repository after validating them.
        """
        for recipe in recipes:
            if not isinstance(recipe, Recipe):
                raise TypeError("Expected a Recipe instance")
            self.__recipes.append(recipe)

    def get_recipe(self) -> List[Recipe]:
        return self.__recipes

    def get_all_recipe_id(self) -> list[int]:
        return [recipe.id for recipe in self.__recipes]

    def get_number_of_recipes(self) -> int:
        return len(self.__recipes)

    def get_recipe_by_id(self, recipe_id:int) -> int:
        for recipe in self.__recipes:
            if recipe.id == recipe_id:
                return recipe
        raise ValueError(f"Recipe with id {recipe_id} not found")

    #endregion

    #region Review_data
    def add_review(self, review: Review):
        user = review.user
        recipe = review.recipe
        current_reviews = self.__reviews[recipe.id]
        for temp in current_reviews:
            if temp.user.username == user.username:
                raise ValueError(f"User '{user.username}' has already reviewed this recipe!")
        self.__reviews[recipe.id].append(review)
        review.user.reviews.append(review)
        review.recipe.reviews.append(review)

    def get_recipe_reviews(self, recipe_id: int):
        self.__reviews.setdefault(recipe_id, [])
        return [r for r in self.__reviews[recipe_id] if r is not None]

    #endregion

    #region User_data
    def add_user(self, user: User):
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")
        if user.id is None:
            user._User__id = self._next_user_id
            self._next_user_id += 1
        self.__users.append(user)

    def get_user(self, username: str) -> User | None:
        for user in self.__users:
            if user.username == username:
                return user
        return None

    #endregion

    #region Favourite
    def add_favourite(self, user: User, recipe: Recipe):
        favourite = Favourite(
            favourite_id=self.__favourite_id_counter,
            user=user,
            recipe=recipe
        )
        self.__favourite_id_counter += 1
        user.add_favourite_recipe(favourite)
        self.__favourites.append(favourite)

    def remove_favourite(self, user: User, recipe: Recipe):
        for favourite in self.__favourites:
            if favourite.user == user and favourite.recipe == recipe:
                self.__favourites.remove(favourite)
                user.remove_favourite_recipe(favourite)
                return

    def get_favourites(self, user: User) -> List[Favourite]:
        return [recipe for recipe in self.__favourites if recipe.user == user]

    #endregion

    #region RecipeSearch
    def get_recipes(self, page: int, per_page: int, search_query: str, search_type: str = 'name') -> List[Recipe]:
        recipes = self.__recipes
        if search_query:
            search_query_lower = search_query.lower()
            if search_type == "name":
                recipes = [r for r in recipes if search_query_lower in r.name.lower()]
            elif search_type == "author":
                recipes = [r for r in recipes if r.author and hasattr(r.author, 'name') and search_query_lower in r.author.name.lower()]
            elif search_type == "category":
                recipes = [r for r in recipes if r.category and hasattr(r.category, 'name') and search_query_lower in r.category.name.lower()]
            elif search_type == "id":
                try:
                    search_id = int(search_query)
                    recipes = [r for r in recipes if r.id == search_id]
                except ValueError:
                    recipes = []

        start = (page - 1) * per_page
        end = start + per_page
        pagination = recipes[start:end]
        return pagination

    def get_recipe_count(self, search_query: str, search_type: str = "name") -> int:
        recipes = self.__recipes
        if search_query:
            search_query_lower = search_query.lower()
            if search_type == "name":
                recipes = [r for r in recipes if search_query_lower in r.name.lower()]
            elif search_type == "author":
                recipes = [r for r in recipes if r.author and hasattr(r.author, 'name') and search_query_lower in r.author.name.lower()]
            elif search_type == "category":
                recipes = [r for r in recipes if r.category and hasattr(r.category, 'name') and search_query_lower in r.category.name.lower()]
            elif search_type == "id":
                try:
                    search_id = int(search_query)
                    recipes = [r for r in recipes if r.id == search_id]
                except ValueError:
                    recipes = []

        return len(recipes)

    #endregion