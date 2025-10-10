from pathlib import Path

from recipe.adapters import database_repository
from recipe.adapters.Repository import AbstractRepository
from recipe.adapters.datareader.csv_parser import CSVDataReader




def populate(repo: AbstractRepository, database_mode : bool):
    BASE_DIR = Path(__file__).resolve().parent
    filepath = BASE_DIR.parent / "adapters" / "datareader" / "data" / "recipes.csv"
    reader = CSVDataReader(str(filepath))
    reader.read_recipes_csv()
    if database_mode:
        if isinstance(repo, database_repository.SqlAlchemyRepository):
            repo.add_multiple_recipes(reader.dataset_of_recipes)
            repo.add_multiple_authors(reader.dataset_of_authors)
            repo.add_multiple_categories(reader.dataset_of_categories)
    else:
        for recipe in reader.dataset_of_recipes:
            repo.add_recipe(recipe)