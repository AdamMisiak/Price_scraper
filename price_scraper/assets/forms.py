from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField



class CheckPriceForm(FlaskForm):

    quantity_btc = FloatField('Quantity of BTC')
    quantity_xrp = FloatField('Quantity of XRP')
    quantity_xlm = FloatField('Quantity of XLM')
    quantity_gld = FloatField('Quantity of GLD')

    submit = SubmitField('Submit')
