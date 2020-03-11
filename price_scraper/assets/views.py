from flask import Flask, render_template, redirect, url_for, session, Blueprint
from price_scraper.assets.forms import  CheckPriceForm
from price_scraper.assets.functions import check_name_btc,check_name_xlm,check_name_gld,check_name_xrp,check_price_btc,\
                      check_price_gld,check_price_usd,check_price_xlm,check_price_xrp,my_coin_value_pln,my_coin_value_usd,\
                      round_quantity
from price_scraper.models import Asset, User
from price_scraper import app, db
from flask_login import login_user, current_user, logout_user, login_required

assets_blueprint = Blueprint('assets',__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():

    prices = [check_price_btc(), check_price_xrp(), check_price_xlm(), check_price_gld()]

    return render_template('index.html', prices=prices)


@app.route('/add_asset', methods=['GET', 'POST'])
def add_asset():

    form = CheckPriceForm()
    if form.validate_on_submit():

        asset = Asset(quantity_btc = form.quantity_btc.data, quantity_xrp = form.quantity_xrp.data,
                          quantity_xlm = form.quantity_xlm.data, quantity_gld = form.quantity_gld.data,
                          user_id = current_user)

        db.session.add(asset)
        db.session.commit()

        return redirect(url_for('assets.summary'))

    return render_template('add_asset.html', form=form)


@assets_blueprint.route('/summary')
def summary():
    user = current_user
    asset = Asset.query.get(user.asset_id)
    functions = [check_name_btc(), check_name_xrp(), check_name_xlm(), check_name_gld()]
    prices = [check_price_btc(), check_price_xrp(), check_price_xlm(), check_price_gld()]
    return render_template('summary.html', functions=functions, prices=prices, asset=asset)

#HW model asset + templatka, zamien relationship + MIGRACJA!, walidacja ze asset musi miec user id (nie moze byc null)
#TEST niec dziala

@assets_blueprint.route('/list')
def list_assets():
    all_assets = Asset.query.all()
    return render_template('list_a.html', all_assets=all_assets)