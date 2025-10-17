import abc
from typing import List
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

repo_instance = None

class AbstractRepository(abc.ABC):

    #region Author_data

    @abc.abstractmethod
    def add_author(self, author: Author):
        """Adds an Author to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_authors(self) -> list[Author]:
        """Returns a list of all Authors in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_authors(self) -> int:
        """Returns the number of Authors in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_authors(self, authors: List[Author]):
        """Adds multiple Authors to the repository."""
        raise NotImplementedError

    # endregion


    #region Category_data

    @abc.abstractmethod
    def add_category(self, category: Category):
        """Adds a Category to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_categories(self) -> List[Category]:
        """Returns a list of all Categories in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_categories(self) -> int:
        """Returns the number of Categories in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_categories(self, categories: List[Category]):
        """Adds multiple Categories to the repository."""
        raise NotImplementedError

    # endregion


    #region Recipe_data
    @abc.abstractmethod
    def add_recipe(self, recipe: Recipe):
        """ Add recipe to recipe repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_multiple_recipes(self, recipe: List[Recipe]):
        """Adds multiple Recipes to the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe(self) -> List[Recipe]:
        """ Returns the list of recipes"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_recipe_id(self) -> list[int]:
        """ Returns all recipes' id """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_recipes(self) -> int:
        """ Returns the number of recipes """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        """ Returns the recipe by id """
        raise NotImplementedError

    #endregion

    #region Review_data
    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_reviews(self, recipe_id: int):
        """ Returns a list of Reviews for the given recipe. """
        raise NotImplementedError

    #endregion

    #region User_data
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

    #endregion

    #region Favourite_data
    @abc.abstractmethod
    def add_favourite(self, favourite: Favourite):
        """" Adds a Favourite Recipe to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_favourite(self, user: User, recipe: Recipe):
        """" Removes a Favourite Recipe to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_favourites(self, user: User) -> List[Favourite]:
        """" Gets a list of Favourite Recipes to the repository. """
        raise NotImplementedError

    #endregion

    #region RecipeSearch
    @abc.abstractmethod
    def get_recipes(self, page:int, per_page:int, search_query: str, search_type:str = 'name') -> List[Recipe]:
        """" Gets a list of  Recipes to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_recipe_count(self, search_query: str, search_type:str = "name") -> int:
        """" Gets a number of  Recipes to the repository. """
        raise NotImplementedError

    #endregion
