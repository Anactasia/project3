import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Words(SqlAlchemyBase):
    __tablename__ = 'Words'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    word = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    complexity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    id_theme = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("Themes.id"))
    theme = orm.relation('Themes')