import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Tracks(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Track'
    trackid = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    albumid = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("album.albumid"))
    genreid = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("genre.genreid"))
    composer = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    milliseconds = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
