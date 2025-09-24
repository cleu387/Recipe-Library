from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from password_validator import PasswordValidator

from functools import wraps

import recipe.authentication.services as services
import recipe.adapters.Repository as repo

authentication_blueprint = Blueprint("authentication_bp", __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_not_unique = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)

            # If successfully registered user, back to homepage.
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueException:
            username_not_unique = 'Your username is taken. Try another one.'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/register.html',
        title='Register',
        form=form,
        username_error_message=username_not_unique,
        handler_url=url_for('authentication_bp.register')
    )


@authentication_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    authentication_failed = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to look up the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.home'))

        except services.InvalidException:
            # Authentication failed, set a suitable error message.
            authentication_failed = 'Login failed! Please check username and password and try again.'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/login.html',
        title='Login',
        authentication_fail_message = authentication_failed,
        form=form,
    )

@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        username = session.get('username')

        if not username or repo.repo_instance.get_user(username) is None:
            session.clear()
            return redirect(url_for('authentication_bp.login'))

        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            #Incase HTML validation fails
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)

class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Username is required'),
        Length(min=3, message='Username is too short')])

    password = PasswordField('Password', [
        DataRequired(message='Password is required'),
        PasswordValid()])

    verify_password = PasswordField('Verify Password', [
        DataRequired(message='Verify Password is required'),
        EqualTo('password', message='Passwords must match')])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')
