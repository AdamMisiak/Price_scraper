import requests
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

        all_assets = Asset.query.all()
        for asset in all_assets:
            if asset.user_id == None:
                db.session.delete(asset)
                db.session.commit()

        return redirect(url_for('assets.summary'))

    return render_template('add_asset.html', form=form)


@assets_blueprint.route('/summary')
def summary():
    user = current_user
    asset = Asset.query.get(user.asset_id)
    names = ['Bitcoin', 'Ripple', "Stellar", 'Gold']
    quantities = [asset.quantity_btc, asset.quantity_xrp, asset.quantity_xlm, asset.quantity_gld]
    prices = requests.get('http://package/')
    #prices = requests.get('http://127.0.0.1:8000/')

    actual_usd = prices.json()["USD"]

    prices_usd = [prices.json()["BTC"], prices.json()["XRP"], prices.json()["XLM"], prices.json()["GLD"]]

    prices_pln = [round(actual_usd*prices_usd[0], 3), round(actual_usd*prices_usd[1], 3),
                  round(actual_usd*prices_usd[2], 3), round(actual_usd*prices_usd[3], 3)]

    values_usd = [round(prices_usd[0]*quantities[0], 3), round(prices_usd[1]*quantities[1], 3),
                  round(prices_usd[2]*quantities[2], 3), round(prices_usd[3]*quantities[3], 3)]

    values_pln = [round(actual_usd*values_usd[0], 3), round(actual_usd*values_usd[1], 3),
                  round(actual_usd*values_usd[2], 3), round(actual_usd*values_usd[3], 3)]

    parts = [round((values_usd[0]/(values_usd[0]+values_usd[1]+values_usd[2]+values_usd[3]))*100, 3),
             round(values_usd[1]/(values_usd[0]+values_usd[1]+values_usd[2]+values_usd[3])*100, 3),
             round(values_usd[2]/(values_usd[0]+values_usd[1]+values_usd[2]+values_usd[3])*100, 3),
             round(values_usd[3]/(values_usd[0]+values_usd[1]+values_usd[2]+values_usd[3])*100, 3)]

    total = values_pln[0]+values_pln[1]+values_pln[2]+values_pln[3]

    return render_template('summary.html', names=names, quantities=quantities, prices_usd=prices_usd,
                           prices_pln=prices_pln, values_usd=values_usd, values_pln=values_pln, parts=parts,
                           total=total)


@assets_blueprint.route('/list')
def list_assets():
    all_assets = Asset.query.all()
    return render_template('list_a.html', all_assets=all_assets)