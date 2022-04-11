import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
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


    # def set_password(self, password):
    #     self.hashed_password = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.hashed_password, password)
