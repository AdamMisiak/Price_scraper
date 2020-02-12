from flask import Flask, render_template, request, redirect, url_for, session
from forms import CheckPriceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'

@app.route('/',methods=['GET','POST'])
def index():

    form = CheckPriceForm()
    if form.validate_on_submit():
        session['quantity_btc'] = form.quantity_btc.data
        session['quantity_xrp'] = form.quantity_xrp.data
        session['quantity_xlm'] = form.quantity_xlm.data
        session['quantity_gld'] = form.quantity_gld.data

        session['price_btc_usd'] = form.price_btc_usd
        session['name_btc'] = form.name_btc
        session['price_xrp_usd'] = form.price_xrp_usd
        session['name_xrp'] = form.name_xrp
        session['price_xlm_usd'] = form.price_xlm_usd
        session['name_xlm'] = form.name_xlm
        session['price_gld_usd'] = form.price_gld_usd
        session['name_gld'] = form.name_gld

        session['price_btc_pln'] = form.price_btc_pln
        session['price_xrp_pln'] = form.price_xrp_pln
        session['price_xlm_pln'] = form.price_xlm_pln
        session['price_gld_pln'] = form.price_gld_pln

        session['coin_value_usd'] = session['price_btc_usd'] * session['quantity_btc']

        return redirect(url_for('summary'))

    return render_template('index.html',form=form)

@app.route('/summary')
def summary():
    return render_template('summary.html')



if __name__ == '__main__':
    app.run(debug=True)
