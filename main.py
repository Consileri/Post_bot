from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user

from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from config import code_for_validation
from data import db_session
from data.mailbox_send import Mail
from data.oder import Order
from forms.mailbox_send import MailForm
from forms.order import OrderForm
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.orders_list import ListForm
from data.users import User
from forms.order_status import StatusForm
from forms.validate import ValidateForm
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.sqlite")
    app.run()


@app.route('/')
def index():
    session = db_session.create_session()

    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        if form.selection.data == 'customer':
            user = User(
                name=form.name.data,
                email=form.email.data,
                is_postman=form.selection.data == "postman"
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            login_user(user)
            return redirect('/')
        elif form.selection.data == 'postman':
            form_1 = ValidateForm()
            form_1.email.data = form.email.data
            form_1.password.data = form.password.data
            form_1.password_again.data = form.password_again.data
            form_1.name.data = form.name.data
            form_1.selection.data = form.selection.data
            return render_template('validate.html', title='Валидация', form=form_1)
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/validate', methods=['GET', 'POST'])
def validate():
    form = ValidateForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if form.code.data == code_for_validation:
            user = User(
                name=form.name.data,
                email=form.email.data,
                is_postman=form.selection.data == "postman"
            )
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            login_user(user)
            return redirect('/')
        return render_template('validate.html', title='Валидация', form=form, message='Неверный код')
    return render_template('validate.html', title='Валидация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('help.html')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    return render_template('contacts.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/list', methods=['GET', 'POST'])
def orders_list():
    session = db_session.create_session()
    orders = session.query(Order)
    session.merge(current_user)
    session.commit()
    return render_template('orders_list.html',
                           orders=orders)


@app.route('/postman/<int:id>', methods=['GET', 'POST'])
def postman(id):
    form = StatusForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        order = session.query(Order).filter(Order.id == id).first()
        if order:
            order.is_adopted = form.statuses.data == 'adopted'
            order.is_getting_ready = form.statuses.data == 'getting_ready'
            order.is_delivering = form.statuses.data == 'delivering'
            order.is_waiting = form.statuses.data == 'waiting'
            order.is_done = form.statuses.data == 'done'
            order.is_not_adopted = form.statuses.data == 'not_adopted'
            session.commit()
            return redirect('/list')
        else:
            abort(404)
    return render_template('order_status.html', form=form)


@app.route('/customer', methods=['GET', 'POST'])
def customer():
    form = OrderForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        order = Order()
        order.country = form.country.data
        order.town = form.town.data
        order.street = form.street.data
        order.house = form.house.data
        order.flat = form.flat.data
        order.body = form.body.data
        order.porch = form.porch.data
        order.floor = form.floor.data
        order.your_name = form.your_name.data
        order.phone = form.phone.data
        order.id = randint(1000000, 9999999)
        current_user.order.append(order)
        session.merge(current_user)
        session.commit()
        return redirect('/orders')
    return render_template('order.html', title='Добавленные заказы',
                           form=form)


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    session = db_session.create_session()

    if current_user.is_authenticated:
        orders = session.query(Order).filter(
            (Order.user == current_user))
    else:
        orders = session.query(Order)
    return render_template("your_orders.html", orders=orders)


@app.route('/orders/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_orders(id):
    form = OrderForm()
    if request.method == "GET":
        session = db_session.create_session()
        orders = session.query(Order).filter(Order.id == id,
                                             Order.user == current_user).first()
        if orders:
            form.country.data = orders.country
            form.town.data = orders.town
            form.street.data = orders.street
            form.house.data = orders.house
            form.flat.data = orders.flat
            form.body.data = orders.body
            form.porch.data = orders.porch
            form.floor.data = orders.floor
            form.your_name.data = orders.your_name
            form.phone.data = orders.phone
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        orders = session.query(Order).filter(Order.id == id,
                                             Order.user == current_user).first()
        if orders:
            orders.country = form.country.data
            orders.town = form.town.data
            orders.street = form.street.data
            orders.house = form.house.data
            orders.flat = form.flat.data
            orders.body = form.body.data
            orders.porch = form.porch.data
            orders.floor = form.floor.data
            orders.your_name = form.your_name.data
            orders.phone = form.phone.data
            session.commit()
            return redirect('/orders')
        else:
            abort(404)
    return render_template('order.html', title='Редактирование заказа', form=form)


@app.route('/orders_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def orders_delete(id):
    session = db_session.create_session()
    orders = session.query(Order).filter(Order.id == id,
                                         Order.user == current_user).first()
    if orders:
        session.delete(orders)
        session.commit()
    else:
        abort(404)
    return redirect('/orders')


@app.route('/mailbox_send', methods=['GET', 'POST'])
@login_required
def mailbox_send():
    form = MailForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        mail = Mail()
        mail.email = form.email.data
        mail.content = form.content.data
        mail.email_sender = current_user.email
        mail.id = randint(1000000, 9999999)
        current_user.mail.append(mail)
        session.merge(current_user)
        session.commit()
        return redirect('/mailbox')
    return render_template('mail_send.html', title='Написать письмо',
                           form=form)


@app.route('/mailbox_rec', methods=['GET', 'POST'])
@login_required
def mailbox_rec():
    session = db_session.create_session()
    mails = session.query(Mail).filter(Mail.email == current_user.email)
    session.commit()
    return render_template("mail_rec.html", mails=mails)


@app.route('/mailbox', methods=['GET', 'POST'])
def mailbox():
    return render_template('mailbox.html')


@app.route('/mail_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def mail_delete(id):
    session = db_session.create_session()
    mails = session.query(Mail).filter(Mail.id == id,
                                       Mail.user == current_user).first()

    if mails:
        session.delete(mails)
        session.commit()
    else:
        abort(404)
    return redirect('/mailbox')


@app.route('/mailbox_from_me', methods=['GET', 'POST'])
@login_required
def mail_from_me():
    session = db_session.create_session()
    mails = session.query(Mail).filter(Mail.email_sender == current_user.email)
    session.commit()
    return render_template("mail_rec.html", mails=mails)


@app.route('/reply/<int:id>', methods=['GET', 'POST'])
@login_required
def reply(id):
    form = MailForm()
    if request.method == "GET":
        return redirect('/mailbox_send')

    if form.validate_on_submit():
        form = MailForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            mail = Mail()
            mail.email = form.email.data
            mail.content = form.content.data
            mail.email_sender = current_user.email
            mail.id = randint(1000000, 9999999)
            current_user.mail.append(mail)
            session.merge(current_user)
            session.commit()
            return redirect('/mailbox')
        return render_template('mail_send.html', title='Написать письмо',
                               form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


if __name__ == '__main__':
    main()
