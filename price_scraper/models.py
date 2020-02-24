from flask_login import UserMixin
from price_scraper import db


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    quantity_btc = db.Column(db.Float)
    quantity_xrp = db.Column(db.Float)
    quantity_xlm = db.Column(db.Float)
    quantity_gld = db.Column(db.Float)

    def __init__(self,quantity_btc,quantity_xrp,quantity_xlm,quantity_gld):
        self.quantity_btc = quantity_btc
        self.quantity_xrp = quantity_xrp
        self.quantity_xlm = quantity_xlm
        self.quantity_gld = quantity_gld



    def __repr__(self):
        return f"BTC quantity= {self.quantity_btc}, XRP quantity= {self.quantity_xrp}, XLM quantity= {self.quantity_xlm}, GLD quantity= {self.quantity_gld}"
