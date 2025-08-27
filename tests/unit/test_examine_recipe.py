def test_view_recipe(client):
    response = client.get("/recipe/38")
    assert response.status_code == 200
    assert b"<h1>" in response.data
    assert b"Author:" in response.data
    assert b"Description:" in response.data
    assert b"Cooking Time:" in response.data
    assert b"Ingredients" in response.data
    assert b"Instructions" in response.data


def test_view_recipe_img_and_nutrition(client):
    response = client.get("/recipe/38")
    assert b"<img" in response.data
    assert b"Calories" in response.data
    assert b"Protein" in response.data
    assert b"Fat" in response.data
    assert b"Carbohydrates" in response.data
    assert b"Saturated Fat" in response.data
    assert b"Cholesterol" in response.data
    assert b"Sodium" in response.data
    assert b"Fiber" in response.data
    assert b"Sugar" in response.data