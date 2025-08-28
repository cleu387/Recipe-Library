import pytest
import random
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

@pytest.fixture
def set_random_seed():
    random.seed(30)
    return random

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

def test_get_recipe_by_id_found():
    mem_repo = MemoryRepository()
    class TestRecipe:
        def __init__(self,id,name):
            self.id = id
            self.name = name

    recipe = TestRecipe(38,"Test Recipe")
    mem_repo._recipes = [recipe]
    result = services.get_recipe_by_id(38, mem_repo)

    assert result is None
    assert recipe.name == "Test Recipe"
    assert recipe.id == 38

def test_get_recipe_by_id_not_found():
    mem_repo = MemoryRepository()
    mem_repo._recipes = []
    result = services.get_recipe_by_id(1, mem_repo)
    assert result is None

def test_get_random_recipe(repository, set_random_seed):
    all_id = repository.get_all_recipe_id()
    random_id = random.choice(all_id)

    recipe = repository.get_recipe_by_id(random_id)

    assert recipe is not None
    assert recipe.id == random_id









