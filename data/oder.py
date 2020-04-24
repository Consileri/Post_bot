import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'order'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    town = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    street = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    house = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flat = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    body = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    porch = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    floor = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    your_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    is_not_adopted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_adopted = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_getting_ready = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_delivering = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_waiting = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_done = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
