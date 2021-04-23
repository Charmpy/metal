import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Albums(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'album'
    albumid = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    artistid = sqlalchemy.Column(sqlalchemy.Integer,
                              sqlalchemy.ForeignKey("artist.artistid"))
    raiting= sqlalchemy.Column(sqlalchemy.Integer)
