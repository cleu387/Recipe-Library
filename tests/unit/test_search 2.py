import pytest

def test_search_by_name(client):
    response = client.get("/browse?search=chocolate&search_type=name")
    assert response.status_code == 200
    assert b"chocolate" in response.data.lower()

def test_search_by_author(client):
    response = client.get("/browse?search=john&search_type=author")
    assert response.status_code == 200
    assert b"john" in response.data.lower()

def test_search_by_category(client):
    response = client.get("/browse?search=dessert&search_type=category")
    assert response.status_code == 200
    assert b"dessert" in response.data.lower()

def test_search_by_valid_id(client):
    response = client.get("/browse?search=40&search_type=id'")
    assert response.status_code == 200
    assert b"best lemonade" in response.data.lower()

def test_search_by_invalid_id(client):
    response = client.get("/browse?search=xyz&search_type=id")
    assert response.status_code == 200
    assert b'no recipes found' in response.data.lower() or b'' in response.data

def test_search_with_empty_query(client):
    response = client.get("/browse")
    assert response.status_code == 200
    assert b'recipe' in response.data.lower()


