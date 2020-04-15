from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class OrderForm(FlaskForm):
    title = StringField('Код заказа:', validators=[DataRequired()])
    submit = SubmitField('Заказать')
