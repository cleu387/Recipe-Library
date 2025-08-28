import pytest
from recipe import create_app
from recipe.adapters.MemoryRepository import MemoryRepository, populate
import recipe.adapters.Repository as repo

#create a test client with an in-memory repository and test data for isolated testing
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    with app.test_client() as client:
        yield client
