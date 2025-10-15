import pytest
import random
import recipe.adapters.Repository as repo
import recipe.browse.services as browse_services
import recipe.home.services as home_services
import recipe.users.services as users_services
from recipe.authentication import services as auth_services
from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters import populate
from recipe.authentication.services import InvalidException
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe

@pytest.fixture
def repository():
    repo.repo_instance = MemoryRepository()
    populate.populate(repo.repo_instance, False)
    return repo.repo_instance

def test_get_number_of_recipes(repository):
    length = repository.get_number_of_recipes()
    assert browse_services.get_number_of_recipes(repository) == length
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
#Test for an ID that does link to a recipe
def test_get_recipe_by_id_found(repository):
    test_id = 38
    recipe = browse_services.get_recipe_by_id(test_id, repository)

    assert recipe.id == 38
#Test for an ID that does not link to a recipe
def test_get_recipe_by_id_not_found():
    recipe_id = 1
    mem_repo = MemoryRepository()
    mem_repo._recipes = []
    with pytest.raises(ValueError):
        browse_services.get_recipe_by_id(recipe_id, mem_repo)

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

def test_can_add_user(repository):
    new_username = 'Billy'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, repository)








