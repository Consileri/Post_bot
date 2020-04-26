from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user, \
    current_user
from flask_restful import Api
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from random import  randint

from data import db_session
from data.oder import Order
from forms.order import OrderForm
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.orders_list import ListForm
from data.users import User
from forms.order_status import StatusForm

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
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            is_postman=form.selection.data == "value"
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


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
    session = db_session.create_session()
    orders = session.query(Order)
    session.merge(current_user)
    session.commit()
    return render_template('orders_list.html', orders=orders)


@app.route('/postman/<int:id>', methods=['GET', 'POST'])
@login_required
def postman1(id):
    form = StatusForm()
    if request.method == "GET":
        session = db_session.create_session()
        order = session.query(Order).filter(Order.id == id).first()
        if order:
            form.is_adopted.data = order.is_adopted
            form.is_not_adopted.data = order.is_not_adopted
            form.is_getting_ready.data = order.is_getting_ready
            form.is_delivering.data = order.is_delivering
            form.is_waiting.data = order.is_waiting
            form.is_done.data = order.is_done

        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        order = session.query(Order).filter(Order.id == id).first()
        if order:
            order.is_adopted = form.is_adopted.data
            order.is_not_adopted = form.is_not_adopted.data
            order.is_getting_ready = form.is_getting_ready.data
            order.is_delivering = form.is_delivering.data
            order.is_waiting = form.is_waiting.data
            order.is_done = form.is_done.data
            session.commit()
            return redirect('/list')
        else:
            abort(404)
    return render_template('order_status.html', form=form)



@app.route('/customer', methods=['GET', 'POST'])
def postman():
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
        order.id = randint(1, 10000000)
        current_user.order.append(order)
        session.merge(current_user)
        session.commit()
        return redirect('/orders')
    return render_template('order.html', title='Добавленные заказы',
                           form=form)


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orderss():
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
