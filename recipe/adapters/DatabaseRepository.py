from abc import ABC
from typing import List, Type

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction

# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self) -> object:
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Author_data
    def add_author(self, author: Author):
        pass

    def get_authors(self) -> List[Author]:
        pass


    def get_number_of_authors(self) -> int:
        pass

    def add_multiple_authors(self, authors: List[Author]):
        seen_ids = set()
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author.id not in seen_ids:
                        scm.session.merge(author)
                        seen_ids.add(author.id)
            scm.commit()

    # endregion


    # region Category_data

    def add_category(self, category: Category):
        pass


    def get_categories(self) -> List[Category]:
        pass

    def get_number_of_categories(self) -> int:
        pass

    def add_multiple_categories(self, categories: List[Category]):
        pass

    # endregion


    # region Recipe_data

    def add_recipe(self, recipe: Recipe):
        pass

    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
                    scm.session.add(recipe)
            scm.commit()

    def get_recipe(self) -> List[Recipe]:
        return self._session_cm.session.query(Recipe).all()

    def get_all_recipe_id(self) -> list[int]:
        result = self._session_cm.session.query(Recipe.id).all()
        return [row[0] for row in result]

    def get_number_of_recipes(self) -> int:
        return self._session_cm.session.query(Recipe).count()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        recipe = self._session_cm.session.query(Recipe).get(recipe_id)
        if recipe is None:
            raise ValueError(f"Recipe with id {recipe_id} not found")
        return recipe

    # endregion


    # region Review_data
    def add_review(self, review: Review):
        pass

    def get_recipe_reviews(self, recipe_id: int):
        pass


    # endregion


    # region User_data
    def add_user(self, user: User):
        pass

    def get_user(self, username: str) -> User:
        pass

    # endregion


    # region Favourite_data

    def add_favourite(self, user: User, recipe: Recipe) -> Favourite:
        pass

    def remove_favourite(self, user: User, recipe: Recipe):
        pass

    def get_favourites(self, user: User) -> List[Favourite]:
        pass

    # endregion



    def _populate_recipe_data(self, recipe: Recipe):
        """
        Populate a Recipe object with related data (images, ingredients, instructions)
        to maintain consistent domain model interface between memory and database repositories.
        """
        if recipe is None:
            return

        # Use the same session context
        with self._session_cm as scm:
            self._populate_recipe_data_in_session(recipe, scm.session)

    def _populate_recipe_data_in_session(self, recipe: Recipe, session):
        """
        Populate a Recipe object with related data using the provided session.
        """
        if recipe is None:
            return

        # Load and populate images
        recipe_images = session.query(RecipeImage).filter(
            RecipeImage._RecipeImage__recipe_id == recipe.id
        ).order_by(RecipeImage._RecipeImage__position).all()

        if recipe_images:
            image_urls = [img.url for img in recipe_images]
            recipe._Recipe__images = image_urls
        else:
            print(f"DEBUG: No images found for recipe {recipe.id}")

        # TODO: Load and populate ingredients
        recipe_images = session.query(RecipeImage).filter(
            RecipeImage._RecipeImage__recipe_id == recipe.id
        ).order_by(RecipeImage._RecipeImage__position).all()

        if recipe_images:
            image_urls = [img.url for img in recipe_images]
            recipe._Recipe__images = image_urls
        else:
            print(f"DEBUG: No images found for recipe {recipe.id}")

        # TODO: Load and populate instructions
        recipe_images = session.query(RecipeImage).filter(
            RecipeImage._RecipeImage__recipe_id == recipe.id
        ).order_by(RecipeImage._RecipeImage__position).all()

        if recipe_images:
            image_urls = [img.url for img in recipe_images]
            recipe._Recipe__images = image_urls
        else:
            print(f"DEBUG: No images found for recipe {recipe.id}")


    # region RecipeImage Methods
    def add_recipe_image(self, recipe_image: RecipeImage):
        pass

    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        pass

    def get_recipe_images(self, recipe_id: int) -> List[RecipeImage]:
        pass

    # endregion

    # region RecipeIngredient Methods
    def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
        pass

    def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
        pass

    def get_recipe_ingredients(self, recipe_id: int) -> List[RecipeIngredient]:
        pass

    # endregion

    # region RecipeInstruction Methods
    def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
        pass

    def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
        with self._session_cm as scm:
            for recipe_instruction in recipe_instructions:
                scm.session.add(recipe_instructions)
            scm.commit()

    def get_recipe_instructions(self, recipe_id: int) -> List[RecipeInstruction]:
        pass

    # endregion
