import pytest
from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters.populate import populate
import recipe.adapters.Repository as repository
from recipe.domainmodel.favourite import Favourite


@pytest.fixture
def repo():
    repository.repo_instance = MemoryRepository()
    populate(repository.repo_instance, False)
    return repository.repo_instance

def test_profile_requires_login(client):
    response = client.get('/profile')
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

def test_profile(client, auth, repo):
    # Register and login to access profile page
    auth.register()
    auth.login()

    user = repo.get_user('Edwin')
    recipe = repo.get_recipe()[0]
    favourite = Favourite(user=user, recipe=recipe)

    # Add a recipe to favourite list
    repo.add_favourite(favourite)

    response = client.get('/profile')
    assert response.status_code == 200
    assert bytes(recipe.name, 'utf-8') in response.data

def test_remove_favourite_recipe(client, auth, repo):
    auth.register()
    auth.login()

    user = repo.get_user('Edwin')
    recipe = repo.get_recipe()[0]
    favourite = Favourite(user=user, recipe=recipe)
    recipe_id = recipe.id

    repo.add_favourite(favourite)
    response = client.post(f'/profile/remove/{recipe_id}')

    assert response.status_code == 302
    assert bytes(recipe.name, 'utf-8') not in response.data