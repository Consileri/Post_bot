from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField
from wtforms.validators import DataRequired


class StatusForm(FlaskForm):
    statuses = RadioField('Label', choices=[('adopted', 'Принят'), ('getting_ready', 'Готовится к отправке'),
            ('delivering', 'Доставляется'), ('waiting', 'Ожидает отгрузки'), ('done', 'Завершен'), ('not_adopted', 'Пока не принят')])
    submit = SubmitField('Изменить')
