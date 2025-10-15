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
        self.__reviews = list()
        self.__users = list()
        self.__tags = list()
        self.__favourite_id_counter = 1
        self.__favourites = list()
        self._next_user_id = 1
        self._next_category_id = 1
        self._next_tag_id = 1

    #region Authors_data
    def add_author(self, author: Author):
        self._validate_author(author)
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
        self._validate_category(category)
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
        self._validate_recipe(recipe)
        self.__recipes.append(recipe)

    def add_multiple_recipes(self, recipes: List[Recipe]):
        """
        Adds multiple Recipes to the repository after validating them.
        """
        for recipe in recipes:
            if not isinstance(recipe, Recipe):
                raise TypeError("Expected a Recipe instance")
            self._validate_recipe(recipe)
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
        self._validate_user(user)
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

    #region Validation
    def _validate_author(self, author: Author):
        if not isinstance(author, Author):
            raise TypeError("Expected an Author instance")
        if author in self.__authors:
            raise FileExistsError(
                f"Author {author.name} already exists in repository")
        if not author.name:
            raise ValueError("Author name cannot be empty")
        if not isinstance(author.name, str):
            raise TypeError("Author name must be a string")
        if author.id < 0:
            raise ValueError("Author ID must be a non-negative integer")
        if not isinstance(author.recipes, list) or not all(
                isinstance(recipe, Recipe) for recipe in author.recipes):
            raise TypeError(
                "Author recipes must be a list of Recipe instances")
        return

    def _validate_category(self, category: Category):
        if category in self.__categories:
            raise FileExistsError(
                f"Category {category.name} already exists in repository")
        if not category.name:
            raise ValueError("Category name cannot be empty")
        if not isinstance(category.name, str):
            raise TypeError("Category name must be a string")
        return

    def _validate_recipe(self, recipe: Recipe):
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        if recipe.author not in self.__authors:
            raise ValueError(
                f"Author {recipe.author.name} not found in repository")
        if recipe.category not in self.__categories:
            raise ValueError(
                f"Category {recipe.category.name} not found in repository")
        if any(r.id == recipe.id for r in self.__recipes):
            raise FileExistsError(
                f"Recipe with ID {recipe.id} already exists in repository")
        if recipe.rating is not None:
            if not (0 <= recipe.rating <= 5):
                raise ValueError("Rating must be between 0 and 5")
        if not isinstance(recipe.date, datetime):
            raise TypeError("Expected a datetime instance for date")
        if recipe in self.__recipes:
            raise FileExistsError("Recipe already exists in the repository")
        if recipe.id < 0:
            raise ValueError("Recipe ID must be a non-negative integer")
        if not isinstance(recipe.name, str) or not recipe.name:
            raise ValueError("Recipe name must be a non-empty string")
        if not isinstance(recipe.author, Author):
            raise TypeError("Expected an Author instance for author")
        if not isinstance(recipe.category, Category):
            raise TypeError("Expected a Category instance for category")
        if not isinstance(recipe.images, list) or not all(
                isinstance(img, str) for img in recipe.images):
            raise TypeError("Expected a list of strings for images")
        if not isinstance(recipe.ingredients, list) or not all(
                isinstance(ing, str) for ing in recipe.ingredients):
            raise TypeError("Expected a list of strings for ingredients")
        if not isinstance(recipe.ingredient_quantities, list) or not all(
                isinstance(qty, str) for qty in recipe.ingredient_quantities):
            raise TypeError(
                "Expected a list of strings for ingredient quantities")
        if not isinstance(recipe.description, str) or not recipe.description:
            raise ValueError("Recipe description must be a non-empty string")
        if not (isinstance(recipe.rating, float) or recipe.rating is None):
            print(recipe.rating)
            print(type(recipe.rating))
            raise ValueError("Recipe rating must be an float or None")
        return

    def _validate_review(self, review: Review):
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance")
        if review.user not in self.__users:
            raise ValueError(
                f"User {review.user.username} not found in repository")
        if review.recipe not in self.__recipes:
            raise ValueError(
                f"Recipe {review.recipe.name} not found in repository")
        if not (0 <= review.rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        if not isinstance(review.date, datetime):
            raise TypeError("Expected a datetime instance for date")
        return

    def _validate_user(self, user):
        if user in self.__users:
            raise FileExistsError(
                f"User {user.username} already exists in repository")
        if user.username in [u.username for u in self.__users]:
            raise FileExistsError(
                f"Username {user.username} already exists in repository")
        if not user.username:
            raise ValueError("Username cannot be empty")
        if not isinstance(user.username, str):
            raise TypeError("Username must be a string")
        if not user.password:
            raise ValueError("Password cannot be empty")
        if not isinstance(user.password, str):
            raise TypeError("Password must be a string")
        return

