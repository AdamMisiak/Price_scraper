from flask import Flask,render_template,url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, FloatField


class CheckPriceForm(FlaskForm):

    quantity_btc = FloatField('Quantity of BTC')
    quantity_xrp = FloatField('Quantity of XRP')
    quantity_xlm = FloatField('Quantity of XLM')
    quantity_gld = FloatField('Quantity of GLD')

    price_btc_usd = check_price_btc()
    name_btc = check_name_btc()
    price_xrp_usd = check_price_xrp()
    name_xrp = check_name_xrp()
    price_xlm_usd = check_price_xlm()
    name_xlm = check_name_xlm()
    price_gld_usd = check_price_gld()
    name_gld = check_name_gld()

    price_btc_pln = check_price_usd(check_price_btc())
    price_xrp_pln = check_price_usd(check_price_xrp())
    price_xlm_pln = check_price_usd(check_price_xlm())
    price_gld_pln = check_price_usd(check_price_gld())

    submit = SubmitField('Submit')
