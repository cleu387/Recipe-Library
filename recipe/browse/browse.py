from flask import Blueprint, render_template, request
import recipe.adapters.Repository as repo
import recipe.browse.services as services

browse_blueprint = Blueprint("recipe_bp", __name__)

@browse_blueprint.route("/browse", methods=["GET"])
def browse_recipes():
    page = int(request.args.get("page", 1))
    per_page = 50

    num_recipes = services.get_number_of_recipes(repo.repo_instance)
    all_recipes = services.get_recipe(repo.repo_instance)

    start = (page - 1) * per_page
    end = start + per_page
    recipes_on_page = all_recipes[start:end]
    total_pages = (num_recipes + per_page - 1) // per_page

    return render_template(
        "browse.html",
        title=f"Browse recipes | CS235 Recipe Portal",
        heading="Browse recipes",
        recipes=recipes_on_page,
        num_recipes=num_recipes,
        page=page,
        total_pages=total_pages,
        endpoint="recipe_bp.browse_recipes",
    )

@browse_blueprint.route("/recipe/<int:recipe_id>", methods=["GET"])
def recipeDescription(recipe_id):
    recipe = services.get_recipe_by_id(recipe_id, repo.repo_instance)

    return render_template(
        "recipeDescription.html",
        title=f"Recipe: {recipe.name}",
        recipe=recipe
    )