import pytest
import recipe.adapters.Repository as repository
from recipe.adapters.MemoryRepository import MemoryRepository, populate
import recipe.browse.review_services as services
import recipe.authentication.services as auth_services
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User


@pytest.fixture
def repo():
    repository.repo_instance = MemoryRepository()
    populate(repository.repo_instance)
    return repository.repo_instance

def test_get_no_reviews(client):
    response = client.get("/recipe/3459")
    data = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "No reviews yet :(" in data

def test_add_reviews(client, repo):
    new_username = 'Billy'
    new_password = 'abcd1A23'
    user = User(new_username, new_password)
    recipe = repo.get_recipe_by_id(38)
    review = Review(1, user, recipe, 3, "This is a review")

    auth_services.add_user(new_username, new_password, repo)
    services.get_recipe_reviews(repo, 38)
    services.add_review(repo, review.user, review.recipe, review.rating, review.review_text)

    response = client.get("/recipe/38")
    data = response.data.decode("utf-8")
    assert response.status_code == 200
    assert "Billy" in data
    assert "(3 / 5)" in data
    assert "This is a review" in data
    assert "No reviews yet :(" not in data





