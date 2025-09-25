from flask import Blueprint, render_template, session, redirect, url_for
import recipe.adapters.Repository as repo

from recipe.authentication.authentication import login_required
import recipe.users.services as services


users_blueprint = Blueprint("users_bp", __name__)

@users_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    username = session.get("username")
    favourites_list = services.get_favourites(username, repo.repo_instance)
    favourites = [favourite.recipe for favourite in favourites_list]
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