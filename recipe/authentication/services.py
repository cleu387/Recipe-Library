from werkzeug.security import generate_password_hash, check_password_hash

from recipe.adapters.Repository import AbstractRepository
from recipe.domainmodel.user import User


class NameNotUniqueException(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass

def add_user(username: str, password: str, repo: AbstractRepository):
    # Check that the given username is available.
    new_user = repo.get_user(username)
    if new_user is not None:
        raise NameNotUniqueException

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    new_user = User(username, password_hash)
    repo.add_user(new_user)

def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)

def authenticate_user(username: str, password: str, repo: AbstractRepository):
    authenticated = False

    current_user = repo.get_user(username)
    if User is not None:
        authenticated = check_password_hash(current_user.password, password)
    if not authenticated:
        raise AuthenticationException

# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(new_user: User):
    user_dict = {
        'username': new_user.username,
        'password': new_user.password
    }
    return user_dict