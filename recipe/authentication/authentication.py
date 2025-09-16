from flask import Blueprint, render_template, redirect, url_for, session, request

authentication_blueprint = Blueprint("authentication_bp", __name__)

@authentication_blueprint.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")