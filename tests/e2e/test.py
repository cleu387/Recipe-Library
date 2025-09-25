import pytest



def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200


    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'Bob', 'password': 'Password123', 'verify_password': 'Password123'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

@pytest.mark.parametrize(('username', 'password', 'verify_password', 'message'), (
        ('', '', '', b'Username is required'),
        ('cj', '', '', b'Username is too short'),
        ('test', '', '', b'Password is required'),
        ('test', 'test', '', b'Must contain at least one number and one uppercase and lowercase letter, and minimum of 8 characters'),\
        ('test', 'Test1234', '', b'Verify Password is required'),
        ('test', 'Test1234', 'test', b'Passwords must match'),
        ('test', 'Test1234', 'Test1234', b'Your username is taken. Try another one'),
))

def test_register_with_invalid_input(client, username, password, verify_password, message):
    # Pre-register users if they not exist yet
    if username == 'test' and password == verify_password:
        client.post('/authentication/register', data={
            'username': 'test',
            'password': 'Test1234',
            'verify_password': 'Test1234'
        })

    # Check that attempting to register with invalid combinations of username and password generate appropriate error messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password, 'verify_password': verify_password}
    )
    assert message in response.data

def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    auth.register()
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client.session_transaction() as session:
        assert session['username'] == 'Edwin'

def test_logout(client, auth):
    # Register and Login a user.
    auth.register()
    auth.login()

    with client.session_transaction() as session:
        assert session['username'] == 'Edwin'

    auth.logout()
    with client.session_transaction() as session:
        assert 'username' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Recipe Library' in response.data

def test_login_required_to_view_profile(client):
    response = client.get('/profile')
    assert response.headers['Location'] == '/authentication/login'

"""def test_search_by_id(client):
    recipe_id = 38
    response = client.get("/recipes/search/?search={recipe_id}")
    assert response.status_code == 200
    assert recipe_id in response.data

def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/authentication/login'

def test_health_star_rating(client):
    response = client.get("/get_health_star_rating", data = {"recipe_id": 38})
    assert response.status_code == 200
    assert b"Health Star Rating" in response.data

def test_login(client, auth):

    response = client.get("/login/")
    assert response.status_code == 200

    # Redirects to homepage after logging in
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

"""


