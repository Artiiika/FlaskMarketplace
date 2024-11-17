from flask_sqlalchemy import session, SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()


#  создание таблицы в БД
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    user_email = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(256), nullable=False)
    user_created = db.Column(db.DateTime(datetime.now()))
    user_products = db.relationship('Product', backref='user')

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.user_password, password)

    def __repr__(self):
        return f'{self.user_name}'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    product_desc = db.Column(db.String(250), nullable=False)
    product_price = db.Column(db.Float(), nullable=False)
    product_image = db.Column(db.String(250), nullable=False)
    product_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    product_category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'{self.product_name}'

