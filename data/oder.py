import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'order'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_adopted = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_getting_ready = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_delivering = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_waiting = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_done = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
