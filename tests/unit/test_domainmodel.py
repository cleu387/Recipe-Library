import pytest
from datetime import datetime
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.user import User
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe

# Fixtures
@pytest.fixture
def my_user():
    return User("test user", "password123", 1)


@pytest.fixture
def my_author():
    return Author(1, "Gordon Ramsay")


@pytest.fixture
def my_category():
    return Category("Italian", [], 1)


@pytest.fixture
def my_recipe(my_author, my_category):
    return Recipe(
        recipe_id=1,
        name="Spaghetti Carbonara",
        author=my_author,
        cook_time=20,
        preparation_time=15,
        created_date=datetime(2024, 1, 1),
        description="Classic Italian pasta dish",
        images=["image1.jpg"],
        category=my_category,
        ingredient_quantities=["200g pasta", "100g bacon"],
        ingredients=["pasta", "bacon", "eggs", "cheese"],
        rating=4.5,
        nutrition=None,
        servings="4",
        recipe_yield="4 portions",
        instructions=["Boil pasta", "Cook bacon", "Mix with eggs"]
    )


# User tests
def test_user_construction():
    user = User("john_doe", "secret123", 1)
    assert user.id == 1
    assert user.username == "john_doe"
    assert user.password == "secret123"
    assert user.favourite_recipes == []
    assert user.reviews == []


def test_user_construction_without_id():
    user = User("jane_doe", "password456")
    assert user.id is None
    assert user.username == "jane_doe"


def test_user_equality():
    user1 = User("test", "pass", 1)
    user2 = User("test", "pass", 1)
    user3 = User("test", "pass", 2)
    assert user1 == user2
    assert user1 != user3


def test_user_less_than():
    user1 = User("test", "pass", 1)
    user2 = User("test", "pass", 2)
    assert user1 < user2


def test_user_hash():
    user1 = User("test", "pass", 1)
    user2 = User("test", "pass", 1)
    user_set = {user1, user2}
    assert len(user_set) == 1


# Author tests
def test_author_construction():
    author = Author(1, "Jamie Oliver")
    assert author.id == 1
    assert author.name == "Jamie Oliver"
    assert author.recipes == []


def test_author_equality():
    author1 = Author(1, "Chef A")
    author2 = Author(1, "Chef B")
    author3 = Author(2, "Chef A")
    assert author1 == author2
    assert author1 != author3


def test_author_less_than():
    author1 = Author(1, "Chef A")
    author2 = Author(2, "Chef B")
    assert author1 < author2


def test_author_hash():
    author1 = Author(1, "Chef A")
    author2 = Author(1, "Chef B")
    author_set = {author1, author2}
    assert len(author_set) == 1


def test_author_add_recipe(my_author, my_recipe):
    my_author.add_recipe(my_recipe)
    assert my_recipe in my_author.recipes


def test_author_add_duplicate_recipe(my_author, my_recipe):
    my_author.add_recipe(my_recipe)
    with pytest.raises(ValueError):
        my_author.add_recipe(my_recipe)


# Category tests
def test_category_construction():
    category = Category("Desserts", [], 1)
    assert category.id == 1
    assert category.name == "Desserts"
    assert category.recipes == []


def test_category_construction_without_id():
    category = Category("Main Course")
    assert category.id is None
    assert category.name == "Main Course"


def test_category_equality():
    category1 = Category("Italian", [], 1)
    category2 = Category("French", [], 1)
    category3 = Category("Italian", [], 2)
    assert category1 == category2
    assert category1 != category3


def test_category_less_than():
    category1 = Category("A", [], 1)
    category2 = Category("B", [], 2)
    assert category1 < category2


def test_category_hash():
    category1 = Category("Italian", [], 1)
    category2 = Category("French", [], 1)
    category_set = {category1, category2}
    assert len(category_set) == 1


def test_category_add_recipe(my_category, my_recipe):
    my_category.add_recipe(my_recipe)
    assert my_recipe in my_category.recipes


def test_category_add_invalid_recipe(my_category):
    with pytest.raises(TypeError):
        my_category.add_recipe("not a recipe")


# Recipe tests
def test_recipe_construction(my_author, my_category):
    recipe = Recipe(
        recipe_id=1,
        name="Test Recipe",
        author=my_author,
        cook_time=30,
        preparation_time=15,
        created_date=datetime(2024, 1, 1),
        description="Test description",
        images=["test.jpg"],
        category=my_category,
        ingredient_quantities=["1 cup flour"],
        ingredients=["flour"],
        rating=4.0,
        nutrition=None,
        servings="2",
        recipe_yield="2 portions",
        instructions=["Mix ingredients"]
    )
    assert recipe.id == 1
    assert recipe.name == "Test Recipe"
    assert recipe.author == my_author


def test_recipe_equality():
    author = Author(1, "Chef")

    recipe1 = Recipe(1, "Recipe A", author)
    recipe2 = Recipe(1, "Recipe B", author)
    recipe3 = Recipe(2, "Recipe A", author)

    assert recipe1 == recipe2
    assert recipe1 != recipe3


def test_recipe_less_than():
    author = Author(1, "Chef")

    recipe1 = Recipe(1, "Recipe A", author)
    recipe2 = Recipe(2, "Recipe B", author)

    assert recipe1 < recipe2


def test_recipe_hash():
    author = Author(1, "Chef")

    recipe1 = Recipe(1, "Recipe A", author)
    recipe2 = Recipe(1, "Recipe B", author)

    recipe_set = {recipe1, recipe2}
    assert len(recipe_set) == 1


def test_author_set_recipe(my_author):
    new_recipe = Recipe(200, "New Recipe", my_author)

    my_author.add_recipe(new_recipe)
    assert new_recipe in my_author.recipes


def test_author_set_recipe_invalid_type(my_author):
    with pytest.raises(TypeError):
        my_author.add_recipe("not a recipe")
#Initialise a test Nutrition Object
@pytest.fixture
def nutrition_sample():
    return Nutrition(
        nutrition_id=1,
        calories=200,
        fat=8,
        saturated_fat=3,
        cholesterol=10,
        sodium=5,
        carbohydrates=1,
        fiber=5,
        sugar=12,
        protein=3,
    )
#Tests for correct nutrition values
def test_properties_nutrition(nutrition_sample):
    assert nutrition_sample.id == 1
    assert nutrition_sample.calories == 200
    assert nutrition_sample.fat == 8
    assert nutrition_sample.saturated_fat == 3
    assert nutrition_sample.cholesterol == 10
    assert nutrition_sample.sodium == 5
    assert nutrition_sample.carbohydrates == 1
    assert nutrition_sample.fiber == 5
    assert nutrition_sample.sugar == 12
    assert nutrition_sample.protein == 3
#Tests that the __repr__ output of Nutrition object includes key nutrional information
def test_repr_nutrition(nutrition_sample):
    repr_str = repr(nutrition_sample)
    assert "Calories: 200" in repr_str
    assert "Protein: 3" in repr_str
#Tests if the values of two recipes are and are not equal
def test_equality_nutrition():
    n1 = Nutrition(1,100,5,2,8,20,10,3,2,5)
    n2 = Nutrition(2,100,5,2,8,20,10,3,2,5)
    n3 = Nutrition(3,2,3,4,5,6,7,8,9,10)
    assert n1 == n2
    assert n1 != n3
#Tests if the Nutrition values in one recipe are lower than the other
def test_less_than_nutrition():
    low_cal = Nutrition(1,100,5,2,10,100,20,2,8,6)
    high_cal = Nutrition(2,500,10,5,20,200,32,11,40,22)
    assert low_cal < high_cal
    assert not high_cal < low_cal
#Tests if Nutrition object with the same ID have the same hash and objects with differing IDs have different hashes
def test_hash_nutrition():
    n1 = Nutrition(1,100,5,2,8,20,10,3,2,5)
    n2 = Nutrition(1,200,3,4,55,22,11,33,22,11)
    n3 = Nutrition(3,100,5,2,8,20,10,3,2,5)
    assert hash(n1) == hash(n2)
    assert hash(n1) != hash(n3)

#Mock class to for review and favourite
class MockUser:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"User{self.user_id}"
#Mock class to for review and favourite
class MockRecipe:
    def __init__(self, recipe_id, recipe_name):
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name

    def __eq__(self, other) -> bool:
        return isinstance(other, MockRecipe) and self.recipe_id == other.recipe_id

    def __hash__(self) -> int:
        return hash(self.recipe_id)

    def __repr__(self) -> str:
        return f"Recipe{self.recipe_id}"
#Initialise a test Favourite object
def test_favourite_initialization():
    user = MockUser("Eve")
    recipe = MockRecipe(1, "Recipe B")
    fav = Favourite(favourite_id= 1, user=user, recipe=recipe)

    assert fav.id == 1
    assert fav.user == user
    assert fav.recipe == recipe
#Test ability to add recipe to Favourite
def test_add_recipe_favourite():
    user = User("Bob", "Password123")
    recipe = MockRecipe(2, "Pizza")
    fav = Favourite(favourite_id= 1, user=user, recipe=recipe)
    user.add_favourite_recipe(fav)
    assert fav in user.favourite_recipes
#Test cannot add duplicate recipe to favourite
def test_add_duplicate_recipe_favourite():
    user = User("Bob", "Password123")
    recipe = MockRecipe(101, "Pizza")
    fav = Favourite(favourite_id= 2, user=user, recipe=recipe)
    user.add_favourite_recipe(fav)
    assert user.favourite_recipes.count(fav) == 1
    with pytest.raises(ValueError):
        user.add_favourite_recipe(fav)

#Test remove recipe from Favourite
def test_remove_recipe_favourite():
    user = User("Dave", "Password123")
    r1 = MockRecipe(101, "Chip")
    r2 = MockRecipe(102, "Mustard" )
    fav1 = Favourite(favourite_id= 3, user=user, recipe=r1)
    fav2 = Favourite(favourite_id= 4, user=user, recipe=r2)
    user.add_favourite_recipe(fav1)
    user.add_favourite_recipe(fav2)
    user.remove_favourite_recipe(fav1)
    assert fav1 not in user.favourite_recipes
    assert fav2 in user.favourite_recipes
#Test cannot remove nonexistent recipe from Favourite
def test_remove_nonexistent_recipe_favourite():
    user = User("Bob2", "Password123")
    r1 = MockRecipe(301, "Brick")
    r2 = MockRecipe(302, "Brick2")
    fav1 = Favourite(favourite_id= 3, user=user, recipe=r1)
    fav2 = Favourite(favourite_id= 4, user=user, recipe=r2)
    user.add_favourite_recipe(fav1)
    with pytest.raises(ValueError):
        user.remove_favourite_recipe(fav2)
    assert user.favourite_recipes == [fav1]
#Test if output of __repr__ object includes a User and Recipe
def test_repr_favourite():
    user = MockUser("BobAgain")
    recipe = MockRecipe(402, "Burger")
    fav = Favourite(favourite_id= 5, user=user, recipe=recipe)
    assert repr(fav) == f"{user}: {recipe}"
#Test if two Favourite objects have the same ID then their hash values are the same
def test_hash_favourite():
    user = MockUser("Bob")
    r1 = MockRecipe(301, "Brick")
    fav1 = Favourite(favourite_id= 6, user=user, recipe=r1)
    fav2 = Favourite(favourite_id= 6, user=user, recipe=r1)
    assert hash(fav1) == hash(fav2)

#Initialise a test Review object
def test_review_initialization():
    user = MockUser("Bob")
    recipe = MockRecipe(1, "Burger")
    review = Review(1, user, recipe,5,"edible")

    assert review.id == 1
    assert review.user == user
    assert review.recipe == recipe
    assert review.rating == 5
    assert review.review_text == "edible"
    assert isinstance(review.date, datetime)
#Test if a Review object correctly stores the date
def test_review_custom_data():
    user = MockUser("Bob")
    recipe = MockRecipe(2, "Sushi")
    custom_date = (2025,1,1)
    review = Review(2, user, recipe,4,"edible", created_date=custom_date)

    assert review.date == custom_date
#Test setting a valid rating updates the Review object
def test_review_rating_setter_valid():
    user = MockUser("Bob")
    recipe = MockRecipe(3, "Burger")
    review = Review(3, user, recipe,5,"edible")
    review.rating = 5
    assert review.rating == 5
#Test that setting an invalid values raises a ValueError
def test_review_rating_setter_invalid():
    user = MockUser("Bob")
    recipe = MockRecipe(4, "Burger")
    review = Review(4, user, recipe,5,"edible")
    with pytest.raises(ValueError):
        review.rating = 6
#Test that setting text correctly updates Review object correctly
def test_review_text_setter():
    user = MockUser("Bob")
    recipe = MockRecipe(6, "Burger")
    review = Review(6, user, recipe,5,"ok")
    review.review_text = "ok"
    assert review.review_text == "ok"
#Test __repr__ method of Review returns the expected string format
def test_review_repr():
    user = MockUser("Bob")
    recipe = MockRecipe(7, "Burger")
    review = Review(7, user, recipe,9,"wow")
    expected_repr = f"{user}: {recipe}: 9 - wow"
    assert repr(review) == expected_repr
#Test that Review objects with the same ID produce the same hash value
def test_review_hash():
    user = MockUser("Bob")
    recipe = MockRecipe(8, "Burger")
    review1 = Review(8, user, recipe,4,"crap")
    review2 = Review(8,user,recipe,2,"burnt the kitchen down")
    assert hash(review1) == hash(review2)