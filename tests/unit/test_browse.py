import pytest

from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters.populate import populate
import recipe.adapters.Repository as repo

from pathlib import Path

data_path = Path('tests') / 'data' / 'recipes-excerpt.csv'

repo.repo_instance = MemoryRepository()
populate(data_path, repo.repo_instance, False)



def test_browse_recipes(client):
    # Tests that the recipe browser page exists and has the right recipes on it
    response = client.get("/browse")
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    recipes = repo.repo_instance.get_recipes(page=1, per_page=20, search_query="")
    for r in recipes:
        assert r.name in data


def test_browse_recipes_page2(client):
    # Tests that the 2nd page of the recipe browser exists and contains the right recipes
    response = client.get("/browse?page=2")
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    page1_recipes = repo.repo_instance.get_recipes(page=1, per_page=20, search_query="")
    page2_recipes = repo.repo_instance.get_recipes(page=2, per_page=20, search_query="")

    for r in page1_recipes:
        assert r.name not in data
    for r in page2_recipes:
        assert r.name in data





