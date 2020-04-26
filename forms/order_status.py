from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, BooleanField
from wtforms.validators import DataRequired


class StatusForm(FlaskForm):
    is_adopted = BooleanField('Принят')
    is_not_adopted = BooleanField('Не принят')
    is_getting_ready = BooleanField('Готовится к отправке')
    is_delivering = BooleanField('Доставляется')
    is_waiting = BooleanField('Ожидает отгрузки')
    is_done = BooleanField('Завершен')

    submit = SubmitField('Изменить')