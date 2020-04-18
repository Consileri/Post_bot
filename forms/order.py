from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SubmitField, RadioField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    country = StringField('Страна', validators=[DataRequired()])
    town = StringField('Город', validators=[DataRequired()])
    street = StringField('Улица', validators=[DataRequired()])
    house = StringField('Дом', validators=[DataRequired()])
    flat = StringField('Квартира', validators=[DataRequired()])
    body = StringField('Корпус', validators=[DataRequired()])
    porch = StringField('Подъезд', validators=[DataRequired()])
    floor = StringField('Этаж', validators=[DataRequired()])
    your_name = StringField('Как к Вам обращаться?', validators=[DataRequired()])
    phone = StringField('Укажите Ваш номер телефона', validators=[DataRequired()])
    submit = SubmitField('Заказать')
