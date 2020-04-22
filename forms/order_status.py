from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField
from wtforms.validators import DataRequired


class StatusForm(FlaskForm):
    title = StringField('Измените статус заказа', validators=[DataRequired()])
    statuses = RadioField('Label', choices=[('adopted', 'Принят'), ('getting_ready', 'Готовится к отправке'),
            ('delivering', 'Доставляется'), ('waiting', 'Ожидает отгрузки'), ('done', 'Завершен')])
    submit = SubmitField('Изменить')