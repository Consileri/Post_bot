from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired


class ListForm(FlaskForm):
    submit = SubmitField('Изменить состояние заказа')