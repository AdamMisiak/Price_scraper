from flask import Flask, render_template, redirect, url_for, session, Blueprint
from price_scraper.assets.forms import  CheckPriceForm
from price_scraper.assets.functions import check_name_btc,check_name_xlm,check_name_gld,check_name_xrp,check_price_btc,\
                      check_price_gld,check_price_usd,check_price_xlm,check_price_xrp,my_coin_value_pln,my_coin_value_usd,\
                      round_quantity
from price_scraper.models import Asset
from price_scraper import app, db

assets_blueprint = Blueprint('assets',__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():

    form = CheckPriceForm()
    if form.validate_on_submit():

        # new_asset = Asset(quantity_btc = form.quantity_btc.data,quantity_xrp = form.quantity_xrp.data,
        #                   quantity_xlm = form.quantity_xlm.data,quantity_gld = form.quantity_gld.data)
        #
        # db.session.add(new_asset)
        # db.session.commit()

        session['quantity_btc'] = form.quantity_btc.data
        session['quantity_xrp'] = form.quantity_xrp.data
        session['quantity_xlm'] = form.quantity_xlm.data
        session['quantity_gld'] = form.quantity_gld.data

        session['price_btc_usd'] = check_price_btc()
        session['name_btc'] = check_name_btc()
        session['price_xrp_usd'] = check_price_xrp()
        session['name_xrp'] = check_name_xrp()
        session['price_xlm_usd'] = check_price_xlm()
        session['name_xlm'] = check_name_xlm()
        session['price_gld_usd'] = check_price_gld()
        session['name_gld'] = check_name_gld()

        session['price_btc_pln'] = check_price_usd(check_price_btc())
        session['price_xrp_pln'] = check_price_usd(check_price_xrp())
        session['price_xlm_pln'] = check_price_usd(check_price_xlm())
        session['price_gld_pln'] = check_price_usd(check_price_gld())

        session['btc_value_usd'] = my_coin_value_usd(session['quantity_btc'],session['price_btc_usd'])
        session['xrp_value_usd'] = my_coin_value_usd(session['quantity_xrp'], session['price_xrp_usd'])
        session['xlm_value_usd'] = my_coin_value_usd(session['quantity_xlm'], session['price_xlm_usd'])
        session['gld_value_usd'] = my_coin_value_usd(session['quantity_gld'], session['price_gld_usd'])

        session['btc_value_pln'] = my_coin_value_pln(session['quantity_btc'], session['price_btc_pln'])
        session['xrp_value_pln'] = my_coin_value_usd(session['quantity_xrp'], session['price_xrp_pln'])
        session['xlm_value_pln'] = my_coin_value_usd(session['quantity_xlm'], session['price_xlm_pln'])
        session['gld_value_pln'] = my_coin_value_usd(session['quantity_gld'], session['price_gld_pln'])

        session['total_pln'] = session['gld_value_pln'] + session['xlm_value_pln'] +\
                               session['xrp_value_pln'] + session['btc_value_pln']

        session['total_pln'] = round_quantity(session['total_pln'])

        return redirect(url_for('assets.summary'))

    return render_template('index.html', form=form)


@assets_blueprint.route('/summary')
def summary():
    return render_template('summary.html')
