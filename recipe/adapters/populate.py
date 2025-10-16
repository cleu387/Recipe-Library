from pathlib import Path

from recipe.adapters import DatabaseRepository
from recipe.adapters.Repository import AbstractRepository
from recipe.adapters.datareader.CSVReader import CSVDataReader




def populate(repo: AbstractRepository, database_mode : bool):
    BASE_DIR = Path(__file__).resolve().parent
    filepath = BASE_DIR.parent / "adapters" / "datareader" / "data" / "recipes.csv"
    reader = CSVDataReader(str(filepath))
    reader.read_recipes_csv()
    if database_mode:
        if isinstance(repo, DatabaseRepository.SqlAlchemyRepository):
            repo.add_multiple_recipes(reader.dataset_of_recipes)
            repo.add_multiple_authors(reader.dataset_of_authors)
            repo.add_multiple_categories(reader.dataset_of_categories)

            repo.add_multiple_recipe_images(reader.dataset_of_recipe_images)
    else:
        for recipe in reader.dataset_of_recipes:
            repo.add_recipe(recipe)