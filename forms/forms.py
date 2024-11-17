from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, IntegerField, FloatField, FileField


class RegForm(FlaskForm):
    user_name = StringField('Name')
    user_email = EmailField('Email')
    user_password = PasswordField('Password')
    user_password2 = PasswordField('Repeat password')


class LogForm(FlaskForm):
    user_email = EmailField('Email')
    user_password = PasswordField('Password')


class ProductForm(FlaskForm):
    product_name = StringField('Name')
    product_desc = TextAreaField('Description')
    product_price = FloatField('Price')
    product_img = FileField('Photo')