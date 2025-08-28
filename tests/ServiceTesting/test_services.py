import pytest
import recipe.adapters.Repository as repo
import recipe.browse.services as services
import recipe.home.services as services
from recipe.adapters.MemoryRepository import MemoryRepository, populate
import recipe.adapters.Repository as repo
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe

@pytest.fixture
def repository():
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)
    return repo.repo_instance

def test_get_number_of_recipes(repository):
    length = repository.get_number_of_recipes()
    assert services.get_number_of_recipes(repository) == length

def test_get_recipe(repository):
    recipe_dicts = services.get_recipe(repository)
    assert recipe_dicts is not None
    assert isinstance(recipe_dicts, list)
    recipe = recipe_dicts[0]
    assert recipe is not None
    assert isinstance(recipe, dict)
    assert isinstance(recipe["id"], int)
    assert isinstance(recipe["name"], str)
    assert isinstance(recipe["author"], str)

def test_get_random_recipe(repository):
    recipe_dicts = services.get_recipe(repository)








