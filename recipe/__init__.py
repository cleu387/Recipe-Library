"""Initialize Flask app."""
from datetime import datetime
from flask import Flask, render_template
import recipe.adapters.Repository as repo
from recipe.adapters.MemoryRepository import MemoryRepository, populate




def create_app():
    """Construct the core application."""

    app = Flask(__name__)


    with app.app_context():
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)
    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)


    # Create the Flask app object
    @app.route('/')
    def home():
        return render_template('home.html')





    return app
