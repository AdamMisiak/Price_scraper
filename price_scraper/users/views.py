from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from price_scraper.users.forms import RegistrationForm, LoginForm
from price_scraper.models import User
from price_scraper import app, db

users_blueprint = Blueprint('users',__name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit() and form.validate_email(form.email):
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)

        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@users_blueprint.route('/list')
def list_users():
    all_users = User.query.all()
    return render_template('list.html', all_users=all_users)