from sqlalchemy import select, inspect
from recipe.adapters.orm import mapper_registry


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()

    # Check all required tables are there
    assert 'author' in tables
    assert 'categories' in tables
    assert 'favourite' in tables
    assert 'nutrition' in tables
    assert 'recipe_images' in tables
    assert 'recipe_ingredients' in tables
    assert 'recipes' in tables
    assert 'review' in tables
    assert 'user' in tables



