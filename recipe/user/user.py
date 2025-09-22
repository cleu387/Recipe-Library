from flask import Blueprint, render_template
import recipe.adapters.Repository as repo

#Temp
import recipe.home.services as services


user_blueprint = Blueprint("user_bp", __name__)

@user_blueprint.route("/profile", methods=["GET"])
def profile():
    recipes = [services.get_random_recipe(repo.repo_instance) for _ in range(2)]

    return render_template(
        "user/profile.html",
        recipes=recipes
        )
