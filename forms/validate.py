from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired
from forms.register import RegisterForm


class ValidateForm(RegisterForm):
    email = HiddenField('Почта')
    password = HiddenField('Пароль')
    password_again = HiddenField('Повторите пароль')
    name = HiddenField('Имя пользователя')
    selection = HiddenField('Label')
    submit = HiddenField('Войти')
    code = StringField('Введите код подтверждения', validators=[DataRequired()])
