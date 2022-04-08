import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Themes(SqlAlchemyBase):
    __tablename__ = 'Themes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    theme = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    themes = orm.relation("Worlds", back_populates='theme')
