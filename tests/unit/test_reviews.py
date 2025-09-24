import pytest
import recipe.adapters.Repository as repository
from recipe.adapters.MemoryRepository import MemoryRepository, populate

@pytest.fixture
def repo():
    repository.repo_instance = MemoryRepository()
    populate(repository.repo_instance)
    return repository.repo_instance

def test_review(repo, client):
    resp = client.get('recipe/468/reviews')
    assert resp.status_code == 200
    data = resp.data.decode('utf-8')
    print(data)


