import pytest
import os
from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters import populate
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User

@pytest.fixture
def memory_repository():
    mem_repo = MemoryRepository()
    populate.populate(mem_repo, False)
    return mem_repo

def test_get_recipe(memory_repository):
    # Tests the get_recipe function to confirm that it correctly returns all the recipes in the memory repo
    data = memory_repository.get_recipe()
    assert data is not None
    assert isinstance(data, list)
    recipe = data[0]
    assert isinstance(recipe, Recipe)
    assert recipe.name == "Low-Fat Berry Blue Frozen Dessert"
    assert isinstance(recipe.author, Author)
    assert isinstance(recipe.category, Category)
    assert isinstance(recipe.nutrition, Nutrition)

def test_add_recipe(memory_repository):
    # Tests the add_recipe function to confirm that it correctly adds a recipe to the memory repo
    data = memory_repository.get_recipe()
    length = len(data)
    assert data is not None
    temp_recipe = Recipe(1, "default", Author(1, "default"))
    memory_repository.add_recipe(temp_recipe)
    test_data = memory_repository.get_recipe()
    assert test_data is not None
    assert isinstance(test_data, list)
    assert isinstance(test_data[0], Recipe)
    assert len(test_data) == length + 1
    assert test_data[-1] == temp_recipe

def test_get_number_of_recipes(memory_repository):
    # Tests the get_number_of_recipes function to confirm it returns the correct number of recipes
    data = memory_repository.get_recipe()
    assert data is not None
    print(memory_repository.get_number_of_recipes())
    assert memory_repository.get_number_of_recipes() == len(data)

def test_get_all_recipe_id(memory_repository):
    # Tests the get_all_recipes function to confirm it returns all recipes
    data = memory_repository.get_recipe()
    assert data is not None
    assert memory_repository.get_all_recipe_id() == [data.id for data in data]

def test_get_recipe_by_id(memory_repository):
    # Tests the get_recipe_by_id function to confirm it returns the correct recipe with id
    data = memory_repository.get_recipe()
    assert data is not None
    test_recipe = data[0]
    test_id = test_recipe.id

    assert memory_repository.get_recipe_by_id(test_id) == test_recipe

def test_add_user(memory_repository):
    # Tests the add_user function to confirm that it correctly adds a user to the memory repo
    temp_user = User('Bob', 'Password1234')
    memory_repository.add_user(temp_user)
    test_data = memory_repository.get_user(temp_user.username)

    assert test_data is not None
    assert isinstance(test_data, User)
    assert test_data.username == temp_user.username

def test_get_user(memory_repository):
    # Tests the get_user function to confirm that it correctly gets the correct user to the memory repo
    temp_user = User('Bob', 'Password1234')
    memory_repository.add_user(temp_user)
    test_data = memory_repository.get_user('Bob')

    assert test_data is not None
    assert isinstance(test_data, User)
    assert test_data.username == temp_user.username

def test_add_favourite(memory_repository):
    # Tests the add_favourite function to confirm that it correctly adds the correct recipe to the list
    data = memory_repository.get_recipe()
    recipe = data[0]
    temp_user = User('Bob', 'Password1234')

    memory_repository.add_favourite(temp_user, recipe)
    favourites = memory_repository.get_favourites(temp_user)

    assert len(favourites) == 1
    assert isinstance(favourites[0], Favourite)
    assert isinstance(favourites, list)
    assert favourites[0].user == temp_user
    assert favourites[0].recipe == recipe

def test_remove_favourite(memory_repository):
    # Tests the remove_favourite function to confirm that it correctly removes the correct recipe from the list
    data = memory_repository.get_recipe()
    recipe = data[0]
    temp_user = User('Bob', 'Password1234')

    memory_repository.add_favourite(temp_user, recipe)
    memory_repository.remove_favourite(temp_user, recipe)
    favourites = memory_repository.get_favourites(temp_user)

    assert len(favourites) == 0

def test_get_favourites(memory_repository):
    # Tests the get_favourites function to confirm that it correctly gets the correct recipes from the list that belongs to correct user
    data = memory_repository.get_recipe()
    recipe1 = data[0]
    recipe2 = data[1]
    temp_user = User('Bob', 'Password1234')

    memory_repository.add_favourite(temp_user, recipe1)
    memory_repository.add_favourite(temp_user, recipe2)
    favourites = memory_repository.get_favourites(temp_user)

    assert len(favourites) == 2
    assert isinstance(favourites, list)
    assert favourites[0].user == temp_user

