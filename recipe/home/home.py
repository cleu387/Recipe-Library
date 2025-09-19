from flask import Blueprint, render_template
import recipe.adapters.Repository as repo
import recipe.home.services as services

home_blueprint = Blueprint("home_bp", __name__)

@home_blueprint.route("/", methods=["GET"])
def home():
    recipes = [services.get_random_recipe(repo.repo_instance) for _ in range(2)]

    return render_template(
        "home/home.html",
        recipes=recipes)
