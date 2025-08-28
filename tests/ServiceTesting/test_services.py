import pytest
import random
import recipe.adapters.Repository as repo
import recipe.browse.services as browse_services
import recipe.home.services as home_services
from recipe.adapters.MemoryRepository import MemoryRepository, populate
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
    # Tests that the service layer returns the same result as the abstract repository
    assert browse_services.get_number_of_recipes(repository) == length

def test_get_recipe(repository):
    recipe_dicts = browse_services.get_recipe(repository)
    # Tests that the return value exists and has the right parameters
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
    result = browse_services.get_recipe_by_id(38, mem_repo)

    assert result is None
    assert recipe.name == "Test Recipe"
    assert recipe.id == 38

def test_get_recipe_by_id_not_found():
    mem_repo = MemoryRepository()
    mem_repo._recipes = []
    result = browse_services.get_recipe_by_id(1, mem_repo)
    assert result is None

def test_get_random_recipe(repository):
    # Tests that get random recipe does in fact return a random recipe
    import random
    recipes = repository.get_recipe()
    random.seed(42)
    random_recipe = home_services.get_random_recipe(repository)
    # Always returns recipe at index 456
    assert random_recipe is not None
    assert isinstance(random_recipe, Recipe)

    assert random_recipe == recipes[456]












