from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class MailForm(FlaskForm):
    email = StringField('Почта получателя', validators=[DataRequired()])
    content = TextAreaField("Содержимое письма")
    email_sender = HiddenField('Почта отправителя')
    submit = SubmitField('Отправить')
