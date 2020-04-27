from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from flask_restful import Api
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from config import code_for_validation
from data import db_session
from data.oder import Order
from forms.order import OrderForm
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.orders_list import ListForm
from data.users import User
from forms.order_status import StatusForm
from forms.validate import ValidateForm

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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/list', methods=['GET', 'POST'])
def orders_list():
    form = ListForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        session.merge(current_user)
        session.commit()
        return redirect('/postman')
    return render_template('orders_list.html',
                           form=form)


@app.route('/postman', methods=['GET', 'POST'])
def postman():
    form = StatusForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        order = Order(
            is_adopted=form.statuses.data == "adopted",
            is_getting_ready=form.statuses.data == "getting_ready",
            is_delivering=form.statuses.data == "delivering",
            is_waiting=form.statuses.data == "waiting",
            is_done=form.statuses.data == "done"
        )
        current_user.order.append(order)
        session.merge(current_user)
        session.commit()
        return redirect('/')
    return render_template('order_status.html',
                           form=form)


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


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


if __name__ == '__main__':
    main()
