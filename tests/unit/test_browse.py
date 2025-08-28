import pytest

from recipe.adapters.MemoryRepository import MemoryRepository, populate
import recipe.adapters.Repository as repo



repo.repo_instance = MemoryRepository()
populate(repo.repo_instance)



def test_browse_recipes(client):
    # Tests that the recipe browser page exists and has the right recipes on it
    response = client.get("/browse")
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    first_recipe = repo.repo_instance.get_recipe()[0]
    assert first_recipe.name in data


def test_browse_recipes_page2(client):
    # Tests that the 2nd page of the recipe browser exists and contains the right recipes
    response = client.get("/browse?page=2")
    assert response.status_code == 200
    recipes = repo.repo_instance.get_recipe()
    data = response.data.decode("utf-8")
    assert recipes[0].name not in data
    assert recipes[50].name in data




