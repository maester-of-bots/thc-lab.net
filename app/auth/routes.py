from flask import Blueprint, flash
from flask import render_template, redirect, request, url_for
from flask_login import (
    login_user,
    login_required,
    logout_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.auth import blueprint
from app.auth.models import User




auth = Blueprint('auth', __name__)


@blueprint.route('/login')
def login():
    return render_template('auth/login.html')


@blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    from app.auth.models import User

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(
            url_for('auth_blueprint.login'))  # if the user doesn't exist or password is wrong, reload the page
    else:
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('home_blueprint.index'))


@blueprint.route('/signup')
def signup():
    return render_template('auth/signup.html')


@blueprint.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')

        return redirect(url_for('auth_blueprint.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, username=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth_blueprint.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.index'))
