from recipe.adapters.MemoryRepository import MemoryRepository, populate
import recipe.adapters.Repository as repo



repo.repo_instance = MemoryRepository()
populate(repo.repo_instance)



def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.data.decode("utf-8")
    assert b"Home" in response.data
    assert b"Welcome to the Recipe Library" in response.data
