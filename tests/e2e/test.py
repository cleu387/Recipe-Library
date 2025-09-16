import pytest




def test_search_by_id(client):
    recipe_id = 38
    response = client.get("/recipes/search/?search={recipe_id}")
    assert response.status_code == 200
    assert recipe_id in response.data

def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/authentication/login'

def test_health_star_rating(client):
    response = client.get("/get_health_star_rating", data = {"recipe_id": 38})
    assert response.status_code == 200
    assert b"Health Star Rating" in response.data

def test_login(client, auth):

    response = client.get("/login/")
    assert response.status_code == 200

    # Redirects to homepage after logging in
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'


