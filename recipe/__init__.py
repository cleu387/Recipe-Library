"""Initialize Flask app."""
from datetime import datetime
from flask import Flask, render_template
import recipe.adapters.Repository as repo
from recipe.adapters.MemoryRepository import MemoryRepository
from recipe.adapters.DatabaseRepository import SqlAlchemyRepository
from recipe.adapters.populate import populate
from recipe.adapters.orm import map_model_to_tables, mapper_registry

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool




def create_app():
    """Construct the core application."""

    app = Flask(__name__)

    app.config.from_object('config.Config')


    if app.config['REPOSITORY'] == 'memory':
        repo.repo_instance = MemoryRepository()
        populate(repo.repo_instance, False)

    elif app.config['REPOSITORY'] == 'database':
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri,
                                        connect_args={'check_same_thread': False},
                                        poolclass=NullPool, echo=database_echo)

        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        repo.repo_instance = SqlAlchemyRepository(session_factory)


        if app.config['TESTING'] == True or len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            clear_mappers()
            mapper_registry.metadata.drop_all(database_engine)
            mapper_registry.metadata.create_all(database_engine)

            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            map_model_to_tables()

            populate(repo.repo_instance, True)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            map_model_to_tables()

    with app.app_context():
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .users import users
        app.register_blueprint(users.users_blueprint)


        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        @app.teardown_request
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, SqlAlchemyRepository):
                repo.repo_instance.close_session()

        return app



