from abc import ABC
from typing import List, Type
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review
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


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Author_data
    def add_author(self, author: Author):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                scm.session.merge(author)
            scm.session.commit()

    def get_authors(self) -> List[Author]:
        query = self._session_cm.session.query(Author)

        authors = query.all()
        # Populate all recipes with related data
        return authors

    def get_number_of_authors(self) -> int:
        count = self._session_cm.session.query(Author).count()
        return count

    def add_multiple_authors(self, authors: List[Author]):
        seen_ids = set()
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author.id not in seen_ids:
                        scm.session.add(author)
                        seen_ids.add(author.id)
            scm.commit()

    # endregion


    # region Category_data

    def add_category(self, category: Category):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                scm.session.merge(category)
            scm.commit()

    def get_categories(self) -> List[Category]:
        query = self._session_cm.session.query(Category)

        category = query.all()
        # Populate all recipes with related data
        return category

    def get_number_of_categories(self) -> int:
        count = self._session_cm.session.query(Category).count()
        return count

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()

    # endregion


    # region Recipe_data

    def add_recipe(self, recipe: Recipe):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                scm.session.merge(recipe)
            scm.commit()

    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
                    scm.session.add(recipe)
            scm.commit()

    def get_recipe(self) -> list[Recipe]:
        query = self._session_cm.session.query(Recipe)

        recipes = query.all()
        # Populate all recipes with related data
        for recipe in recipes:
            self._populate_recipe_data(recipe)
        return recipes

    def get_all_recipe_id(self) -> list[int]:
        with self._session_cm as scm:
            return [recipe.id for recipe in scm.session.query(Recipe).all()]

    def get_number_of_recipes(self) -> int:
        return self._session_cm.session.query(Recipe).count()

    def get_recipe_by_id(self, recipe_id: int) -> Recipe:
        recipe = None
        try:
            query = self._session_cm.session.query(Recipe).filter(
                Recipe._Recipe__id == recipe_id)
            recipe = query.one()
            # Populate the recipe with related data for consistent domain model interface
            self._populate_recipe_data(recipe)
        except NoResultFound:
            print(f'Recipe {recipe_id} was not found')

        return recipe

    # endregion


    # region Review_data
    def add_review(self, review: Review):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                user = review.user

                if_exist = scm.session.query(Review).filter_by(user_id=review.user.id, recipe_id=review.recipe.id).first()
                if if_exist:
                    pass
                else:
                    scm.session.add(review)
                    review.recipe.add_review(review)
            scm.commit()

    def get_recipe_reviews(self, recipe_id: int):
        reviews = []
        try:
            reviews = self._session_cm.session.query(Review).filter(
                Review.recipe_id == recipe_id).all()

        except NoResultFound:
            print(f'Recipe {recipe_id} was not found')

        return reviews

    # endregion


    # region User_data
    def add_user(self, user: User):
        if not isinstance(user, User):
            raise TypeError("Expected a User instance")

        with self._session_cm as scm:
            with scm.session.no_autoflush:
                scm.session.merge(user)
            scm.commit()

    def get_user(self, username: str) -> User:
        user = None
        try:
            query = self._session_cm.session.query(User).filter(
                User._User__username == username)
            user = query.one()
            # Populate the recipe with related data for consistent domain model interface

        except NoResultFound:
            pass

        return user

    # endregion


    # region Favourite_data

    def add_favourite(self, favourite: Favourite):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                scm.session.add(favourite)
            scm.commit()

    def remove_favourite(self, user: User, recipe: Recipe):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                favourite = scm.session.query(Favourite).filter_by(
                    _Favourite__user=user,
                    _Favourite__recipe=recipe
                ).first()

                if favourite:
                    scm.session.delete(favourite)
            scm.session.commit()

    def get_favourites(self, user: User) -> List[Favourite]:
        favourites = []
        try:
            query = self._session_cm.session.query(Favourite).filter(
                Favourite.user_id == user.id).all()
            for favourite in query:
                favourites.append(favourite)

        except NoResultFound:
            print(f'List of favourite from {user.username} was not found')

        return favourites

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
            recipe._Recipe__images = []

        # Load and populate ingredients
        recipe_ingredients = session.query(RecipeIngredient).filter(
            RecipeIngredient._RecipeIngredient__recipe_id == recipe.id
        ).all()

        if recipe_ingredients:
            recipe._Recipe__ingredient_quantities = [recipe_ingredient.quantity for recipe_ingredient in recipe_ingredients]
            recipe._Recipe__ingredients = [recipe_ingredient.ingredient  for recipe_ingredient in recipe_ingredients]
        else:
            recipe._Recipe__ingredient_quantities = []
            recipe._Recipe__ingredients = []

        # Load and populate instructions
        recipe_instructions= session.query(RecipeInstruction).filter(
            RecipeInstruction._RecipeInstruction__recipe_id == recipe.id
        )

        if recipe_instructions:
            instructions = [instruction.step for instruction in recipe_instructions]
            recipe._Recipe__instructions = instructions
        else:
            recipe.instructions = []

        # Load and populate reviews
        reviews = session.query(Review).filter(
            Review._Review__recipe == recipe
        ).all()

        if reviews:
            recipe._Recipe__reviews = reviews
        else:
            recipe._Review__recipe = []

    # region RecipeImage Methods
    def add_recipe_image(self, recipe_image: RecipeImage):
        pass

    def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
        with self._session_cm as scm:
            for recipe_image in recipe_images:
                scm.session.add(recipe_image)
            scm.commit()

    def get_recipe_images(self, recipe_id: int) -> List[RecipeImage]:
        pass

    # endregion

    # region RecipeIngredient Methods
    def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
        pass

    def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
        with self._session_cm as scm:
            for recipe_ingredient in recipe_ingredients:
                scm.session.add(recipe_ingredient)
            scm.commit()

    def get_recipe_ingredients(self, recipe_id: int) -> List[RecipeIngredient]:
        pass

    # endregion

    # region RecipeInstruction Methods
    def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
        pass

    def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
        with self._session_cm as scm:
            for recipe_instruction in recipe_instructions:
                scm.session.add(recipe_instruction)
            scm.commit()

    def get_recipe_instructions(self, recipe_id: int) -> List[RecipeInstruction]:
        pass

    # endregion

    #region RecipeSearch Methods
    def get_recipes(self, page=1, per_page=20, search_query=None, search_type="name"):
        session = self._session_cm.session
        query = session.query(Recipe)

        if search_query:
            search_query_lower = f"%{search_query.lower()}%"
            if search_type == "name":
                query = query.filter(func.lower(Recipe._Recipe__name).like(search_query_lower))
            elif search_type == "author":
                query = query.join(Recipe._Recipe__author).filter(func.lower(Author._Author__name).like(search_query_lower))
            elif search_type == "category":
                query = query.join(Recipe._Recipe__category).filter(func.lower(Category._Category__name).like(search_query_lower))
            elif search_type == "id":
                try:
                    search_id = int(search_query)
                    query = query.filter(Recipe._Recipe__id == search_id)
                except ValueError:
                    query = query.filter(False)

        query = query.limit(per_page).offset((page - 1) * per_page)
        recipes_orm = query.all()
        recipes = []
        for recipe in recipes_orm:
            self._populate_recipe_data(recipe)
            recipes.append(recipe)

        return recipes


    def get_recipe_count(self, search_query=None, search_type="name"):
        session = self._session_cm.session
        query = session.query(Recipe)
        if search_query:
            search_query_lower = f"%{search_query.lower()}%"
            if search_type == "name":
                query = query.filter(func.lower(Recipe._Recipe__name).like(search_query_lower))
            elif search_type == "author":
                query = query.join(Recipe._Recipe__author).filter(
                    func.lower(Author._Author__name).like(search_query_lower))
            elif search_type == "category":
                query = query.join(Recipe._Recipe__category).filter(
                    func.lower(Category._Category__name).like(search_query_lower))
            elif search_type == "id":
                if search_query.strip("%").isdigit():
                    query = query.filter(Recipe._Recipe__id == int(search_query.strip("%")))
        return query.count()

    #end region
