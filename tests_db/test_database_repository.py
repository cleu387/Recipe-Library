from datetime import datetime

from recipe.adapters.DatabaseRepository import SqlAlchemyRepository
from recipe.domainmodel.author import Author
from recipe.domainmodel.recipe import Recipe


def test_repository_can_get_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    recipes = repo.get_all_recipes()
    assert len(recipes) == 13


def test_repository_can_add_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # Get existing author and category for test recipes
    authors = repo.get_authors('name')
    categories = repo.get_categories()

    if authors and categories:
        author = authors[0]
        category = categories[0]

        recipe1 = Recipe(5001, 'Test recipe 1', author, 30, 15,
                        datetime(2023, 1, 1), 'Test description', [], category,
                        ['1 cup'], ['flour'], 4.5, None, '4', '1 batch', ['Mix ingredients'])
        recipe2 = Recipe(5002, 'Test recipes 2', author, 45, 20,
                        datetime(2023, 1, 2), 'Test description 2', [], category,
                        ['2 cups'], ['sugar'], 4.0, None, '6', '1 batch', ['Mix and bake'])

        repo.add_recipe(recipe1)
        repo.add_recipe(recipe2)

        assert repo.get_recipe(5001) == recipe1
        assert repo.get_recipe(5002) == recipe2


def test_repository_does_not_retrieve_a_non_existent_recipe(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    recipe = repo.get_recipe(9201901)  # Non-existing recipe id
    assert recipe is None


# TODO: Test you can retrieve a recipe. Tip: Check that the recipe has the expected name and author.
def test_repository_can_retrieve_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    recipe = repo.get_recipe(38)
    assert recipe.name == "Low-Fat Berry Blue Frozen Dessert"
    assert recipe.author.name == "Dancer"

# TODO: Test you can get the number of recipes in the testing file recipes_excerpt.csv.
def test_repository_can_retrieve_recipes_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_recipes = repo.get_number_of_recipes()
    assert number_of_recipes == 13


# TODO: Test you can retrieve all 10 recipes for your browse page.
def test_repository_can_retrieve_all_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    recipes = repo.get_recipes(1,10,"names")
    assert len(recipes) == 10


# TODO: Test you can add authors.
def test_repository_can_add_author(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author1 = Author(12, "Bob")
    author2 = Author(13, "David")
    repo.add_author(author1)
    repo.add_author(author2)

    authors = repo.get_authors('name')
    assert author1 in authors
    assert author2 in authors


# TODO: Test you can retrieve authors.
def test_repository_can_retrieve_authors(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    author1 = Author(12, "ABC")
    author2 = Author(13, "ABCC")
    repo.add_author(author1)
    repo.add_author(author2)

    authors = repo.get_authors('name')
    assert authors[0] == author1
    assert authors[1] == author2


