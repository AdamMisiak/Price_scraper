from price_scraper import db, login_manager
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Asset(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.Integer, primary_key=True)
    quantity_btc = db.Column(db.Float)
    quantity_xrp = db.Column(db.Float)
    quantity_xlm = db.Column(db.Float)
    quantity_gld = db.Column(db.Float)
    user_id = relationship("User", uselist=False)


    def __repr__(self):
        return f"BTC quantity= {self.quantity_btc}, XRP quantity= {self.quantity_xrp}, XLM quantity= {self.quantity_xlm}, GLD quantity= {self.quantity_gld}"

class User(db.Model,UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    asset_id = db.Column(db.Integer, ForeignKey('asset.id'))








