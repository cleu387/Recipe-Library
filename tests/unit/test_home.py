from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters.populate import populate
import recipe.adapters.Repository as repo
from pathlib import Path

data_path = Path('tests') / 'data' / 'recipes-excerpt.csv'


repo.repo_instance = MemoryRepository()
populate(data_path, repo.repo_instance, False)



def test_home(client):
    # Tests that the home page exists and has the right contents on it
    response = client.get("/")
    assert response.status_code == 200
    recipes = repo.repo_instance.get_recipe()
    data = response.data.decode("utf-8")
    assert "Home" in data
    assert "Welcome to the Recipe Library" in data

    # Test if there are 3 featured recipes on the home page
    found = 0
    for recipe in recipes:
        if recipe.name in data:
            found += 1
        if found >= 3:
            break
    assert found == 3
