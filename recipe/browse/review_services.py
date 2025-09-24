from recipe.domainmodel.review import Review
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.user import User
from datetime import datetime
from recipe.adapters.Repository import AbstractRepository

def add_review(repo: AbstractRepository, user:User, recipe:Recipe, rating:int, review_text:str):
    if rating < 0 or rating > 5:
        raise ValueError('Rating must be between 0 and 5!')

    review_id = user.id
    review = Review(
        review_id,
        user,
        recipe,
        rating,
        review_text,
        datetime.now()
    )
    repo.add_review(review)
    return review

def get_recipe_reviews(repo:AbstractRepository, recipe_id:int):
    return repo.get_recipe_reviews(recipe_id)

def get_user(repo:AbstractRepository, username:str):
    return repo.get_user(username)



