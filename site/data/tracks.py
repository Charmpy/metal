import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Track(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tracks'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    albumid = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey(
                                    "albums.id", ondelete='SET DEFAULT'),
                                default=0)
    genreid = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey(
                                    "genres.id", ondelete='SET DEFAULT'),
                                default=0)
    seconds = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
