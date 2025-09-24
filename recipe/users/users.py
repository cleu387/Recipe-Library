from flask import Blueprint, render_template, session, redirect, url_for
import recipe.adapters.Repository as repo

from recipe.authentication.authentication import login_required
import recipe.users.services as services
import recipe.home.services as use1

users_blueprint = Blueprint("users_bp", __name__)

@users_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    username = session.get("username")
    favourites = services.get_favourites(username, repo.repo_instance)
    """recipes = [use1.get_random_recipe(repo.repo_instance) for _ in range(9)]"""

    return render_template(
        "users/profile.html",
        recipes=favourites
        )

@users_blueprint.route("/profile/remove/<int:recipe_id>", methods=["POST"])
@login_required
def remove_favourite(recipe_id):
    username = session.get("username")
    services.remove_favourite_recipe(recipe_id, username, repo.repo_instance)
    return redirect(url_for('users_bp.profile'))