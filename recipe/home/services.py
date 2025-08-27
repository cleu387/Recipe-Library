import random
from recipe.adapters.Repository import AbstractRepository



def get_random_recipe_id(repo: AbstractRepository):
    recipes_id = repo.get_all_recipe_id()

    random_id = random.choice(recipes_id)

    return repo.get_recipe_by_id(random_id)
