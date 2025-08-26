from flask import Blueprint, render_template
browse_blueprint = Blueprint("recipe_bp", __name__)

@browse_blueprint.route("/", methods=["GET"])
def home():
    return render_template(
        "home.html")
