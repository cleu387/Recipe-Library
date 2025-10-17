import pytest
import random
import recipe.adapters.Repository as repo
import recipe.browse.services as browse_services
import recipe.home.services as home_services
import recipe.users.services as users_services
from recipe.authentication import services as auth_services
from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters.populate import populate
from recipe.authentication.services import InvalidException
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from pathlib import Path

data_path = Path('tests') / 'data' / 'recipes-excerpt.csv'

@pytest.fixture
def repository():
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance, False)
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
    random.seed(5)
    random_recipe = home_services.get_random_recipe(repository)
    # Always returns recipe at index
    assert random_recipe is not None
    assert isinstance(random_recipe, Recipe)

    assert random_recipe == recipes[9]

def test_can_add_user(repository):
    new_username = 'Billy'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, repository)

    user_as_dict = auth_services.get_user(new_username, repository)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('scrypt:')

def test_cannot_add_user_with_existing_name(repository):
    username = 'Edwin'
    password = 'EdwinNoLikeCooking101'

    auth_services.add_user(username, password, repository)

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, repository)

def test_authentication_with_valid_credentials(repository):
    new_username = 'Edwin'
    new_password = 'EdwinNoLikeCooking101'

    auth_services.add_user(new_username, new_password, repository)

    try:
        auth_services.authenticate_user(new_username, new_password, repository)

    except InvalidException:
        assert False

def test_authentication_with_invalid_credentials(repository):
    new_username = 'Edwin'
    new_password = 'EdwinNoLikeCooking101'

    auth_services.add_user(new_username, new_password, repository)

    with pytest.raises(auth_services.InvalidException):
        auth_services.authenticate_user(new_username, 'NotARealPassword123', repository)

def test_add_favourites(repository):
    new_username = 'Edwin'
    new_password = 'EdwinNoLikeCooking101'

    auth_services.add_user(new_username, new_password, repository)
    test_recipe = repository.get_recipe()[0]

    browse_services.add_favourite_recipe(test_recipe.id, new_username, repository)
    favourite = repository.get_user(new_username).favourite_recipes
    favourite_recipes = [fav.recipe for fav in favourite]
    assert test_recipe in favourite_recipes

def test_get_favourites(repository):
    new_username = 'Edwin'
    new_password = 'EdwinNoLikeCooking101'

    auth_services.add_user(new_username, new_password, repository)
    test_recipe1 = repository.get_recipe()[0]
    test_recipe2 = repository.get_recipe()[1]

    browse_services.add_favourite_recipe(test_recipe1.id, new_username, repository)
    browse_services.add_favourite_recipe(test_recipe2.id, new_username, repository)

    favourite = users_services.get_favourites(new_username, repository)
    assert test_recipe1 in favourite
    assert test_recipe2 in favourite
    assert test_recipe1 != test_recipe2
    assert isinstance(favourite, list)

def test_remove_favourites(repository):
    new_username = 'Edwin'
    new_password = 'EdwinNoLikeCooking101'

    auth_services.add_user(new_username, new_password, repository)
    test_recipe1 = repository.get_recipe()[0]
    test_recipe2 = repository.get_recipe()[1]

    browse_services.add_favourite_recipe(test_recipe1.id, new_username, repository)
    browse_services.add_favourite_recipe(test_recipe2.id, new_username, repository)

    users_services.remove_favourite_recipe(test_recipe1.id, new_username, repository)
    favourite = users_services.get_favourites(new_username, repository)
    assert test_recipe1 not in favourite
    assert test_recipe2 in favourite
    assert isinstance(favourite, list)

def test_if_favourite_exists(repository):
    new_username = 'Edwin'
    new_password = 'EdwinNoLikeCooking101'

    auth_services.add_user(new_username, new_password, repository)
    user = repository.get_user(new_username)
    test_recipe = repository.get_recipe()[0]

    assert browse_services.if_favourite_exists(test_recipe.id, user, repository) == False

    browse_services.add_favourite_recipe(test_recipe.id, new_username, repository)

    assert browse_services.if_favourite_exists(test_recipe.id, user, repository) == True