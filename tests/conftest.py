import pytest
from recipe import create_app
from recipe.adapters.MemoryRepository import MemoryRepository, populate
import recipe.adapters.Repository as repo

#create a test client with an in-memory repository and test data for isolated testing
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    repo.repo_instance = MemoryRepository()
    populate(repo.repo_instance)

    with app.test_client() as client:
        yield client

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def register(self):
        return self.__client.post('/authentication/register', data={
            'username': 'Edwin',
            'password': 'EdwinNoLikeCooking101',
            'verify_password': 'EdwinNoLikeCooking101'
        })

    def login(self, username='Edwin', password='EdwinNoLikeCooking101', verify_password='EdwinNoLikeCooking101'):
        return self.__client.post(
            'authentication/login',
            data={'username': username, 'password': password, 'verify_password': verify_password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)