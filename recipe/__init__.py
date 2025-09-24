"""Initialize Flask app."""
from datetime import datetime
from flask import Flask, render_template
import recipe.adapters.Repository as repo
from recipe.adapters.MemoryRepository import MemoryRepository, populate




def create_app():
    """Construct the core application."""

    app = Flask(__name__)

    app.config.from_object('config.Config')

    with app.app_context():
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .users import users
        app.register_blueprint(users.users_blueprint)

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)




    return app
