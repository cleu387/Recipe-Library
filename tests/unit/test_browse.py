import pytest
import html
from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters.populate import populate
from recipe.adapters import Repository as repo



repo.repo_instance = MemoryRepository()
populate(repo.repo_instance, False)



def test_browse_recipes(client):
    # Tests that the recipe browser page exists and has the right recipes on it
    response = client.get("/browse")
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    data = html.unescape(data)
    recipe = repo.repo_instance.get_recipes(page=1, per_page=20, search_query="")
    for r in recipe:
        assert html.unescape(r.name) in data



def test_browse_recipes_page2(client):
    # Tests that the 2nd page of the recipe browser exists and contains the right recipes
    response = client.get("/browse?page=2")
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    data = html.unescape(data)

    page1_recipe = repo.repo_instance.get_recipes(page=1,per_page=20, search_query="")
    page2_recipe = repo.repo_instance.get_recipes(page=2,per_page=20, search_query="")

    for r in page1_recipe:
        assert html.unescape(r.name) not in data
    for r in page2_recipe:
        assert html.unescape(r.name) in data




