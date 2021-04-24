import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Artist(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'artists'
    __table_args__ = ({'extend_existing': True})
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
