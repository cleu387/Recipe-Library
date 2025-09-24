from flask import Blueprint, render_template, request, session, redirect, url_for
import recipe.adapters.Repository as repo
import recipe.browse.services as services
from recipe.browse import review_services as review_services
from recipe.authentication.authentication import login_required
from recipe.authentication.authentication import login_required

browse_blueprint = Blueprint("recipe_bp", __name__)

@browse_blueprint.route("/browse", methods=["GET"])
def browse_recipes():
    page = int(request.args.get("page", 1))
    per_page = 20
    search_query = request.args.get("search", "").strip().lower()
    search_type = request.args.get("search_type", "name")

    num_recipes = services.get_number_of_recipes(repo.repo_instance)
    all_recipes = services.get_recipe(repo.repo_instance)

    if search_query:
        if search_type == "name":
            all_recipes = [r for r in all_recipes if search_query in r["name"].lower()]
        elif search_type == "author":
            all_recipes = [r for r in all_recipes if search_query in r["author"].lower()]
        elif search_type == "category":
            all_recipes = [r for r in all_recipes if search_query in (r.get("category") or "").lower()]
        elif search_type == "id":
            try:
                search_id = int(search_query)
                all_recipes = [r for r in all_recipes if r["id"] == search_id]
            except ValueError:
                all_recipes = []

    num_recipes = len(all_recipes)

    start = (page - 1) * per_page
    end = start + per_page
    recipes_on_page = all_recipes[start:end]
    total_pages = (num_recipes + per_page - 1) // per_page

    return render_template(
        "browse/browse.html",
        recipes=recipes_on_page,
        num_recipes=num_recipes,
        page=page,
        total_pages=total_pages,
        endpoint="recipe_bp.browse_recipes",
        search_query=search_query,
        search_type=search_type,
    )

@browse_blueprint.route("/recipe/<int:recipe_id>", methods=["GET"])
def recipeDescription(recipe_id):
    recipe = services.get_recipe_by_id(recipe_id, repo.repo_instance)
    reviews = review_services.get_recipe_reviews(repo.repo_instance, recipe_id)
    username = session.get("username")
    user = review_services.get_user(repo.repo_instance, username)
    return render_template(
        "recipebrowse/recipeDescription.html",
        title=f"Recipe: {recipe.name}",
        recipe=recipe,
        reviews=reviews,
        current_user = user
    )

@browse_blueprint.route("/recipe/<int:recipe_id>/favourites", methods=["POST"])
@login_required
def add_favourites(recipe_id):
    username = session['username']
    services.add_favourite_recipe(recipe_id, username, repo.repo_instance)
    return redirect(
        url_for('recipe_bp.recipeDescription', recipe_id=recipe_id)
    )

@browse_blueprint.route("/recipe/<int:recipe_id>", methods=["POST"])
@login_required
def add_review(recipe_id):
    username= session.get("username")
    user = review_services.get_user(repo.repo_instance, username)
    recipe = services.get_recipe_by_id(recipe_id, repo.repo_instance)
    rating = int(request.form.get("rating"))
    text = request.form.get("text")

    message = None
    try:
        review_services.add_review(repo.repo_instance, user, recipe, rating, text)
        message = "Review submitted successfully!"
    except ValueError as e:
        message = str(e)

    reviews = review_services.get_recipe_reviews(repo.repo_instance, recipe_id)
    return redirect(url_for("recipe_bp.recipeDescription", recipe_id=recipe_id))
