from flask import Blueprint, render_template
import recipe.adapters.Repository as repo
import recipe.home.services as services



import random

from recipe.domainmodel.recipe import Recipe

home_blueprint = Blueprint("home_bp", __name__)

@home_blueprint.route("/", methods=["GET"])
def home():
    recipes = [services.get_random_recipe_id(repo.repo_instance) for _ in range(2)]


    return render_template(
        "home.html",
        recipes=recipes)
