import pytest
import os
from recipe.adapters.Repository import AbstractRepository
from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe

@pytest.fixture
def memory_repository():
    mem_repo = MemoryRepository()
    return mem_repo

def test_get_recipe(memory_repository):
    data = memory_repository.get_recipe()
    assert data is not None
    assert isinstance(data, list)
    assert isinstance(data[0], Recipe)
    recipe = data[0]
    assert recipe.name == "Low-Fat Berry Blue Frozen Dessert"
    assert isinstance(recipe.author, Author)
    assert isinstance(recipe.category, Category)
    assert isinstance(recipe.nutrition, Nutrition)



def test_add_recipe(memory_repository):
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
    data = memory_repository.get_recipe()
    assert data is not None
    print(memory_repository.get_number_of_recipes())
    assert memory_repository.get_number_of_recipes() == len(data)


