from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from price_scraper.users.forms import RegistrationForm, LoginForm, UpdateForm
from price_scraper.models import User
from price_scraper.token import generate_confirmation_token, confirm_token
from price_scraper import app, db
from werkzeug.security import generate_password_hash, check_password_hash

users_blueprint = Blueprint('users',__name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=generate_password_hash(form.password.data),
                    )

        db.session.add(user)
        db.session.commit()

        # token = generate_confirmation_token(user.email)

        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not check_password_hash(user.password, form.password.data):
            print('Invalid username or password')
            return redirect(url_for('users.login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@users_blueprint.route('/list')
def list_users():
    all_users = User.query.all()
    # for user in all_users:
    #     if user.asset_id is None:
    #         db.session.delete(user)
    #         db.session.commit()

    return render_template('list.html', all_users=all_users)


@users_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = current_user
    return render_template('account.html', user=user)


@users_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        return redirect(url_for('users.account'))
    return render_template('update.html', form=form)

@users_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))