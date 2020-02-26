from flask import Flask, render_template, redirect, url_for, session, Blueprint
from price_scraper.users.forms import RegistrationForm
from price_scraper.models import User
from price_scraper import app, db

users_blueprint = Blueprint('users',__name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    return render_template('register.html', form=form)
