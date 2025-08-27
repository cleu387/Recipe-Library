import pytest
from recipe import create_app
from recipe.adapters.MemoryRepository import MemoryRepository, populate
import recipe.adapters.Repository as repo

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    with app.test_client() as client:
        yield client
