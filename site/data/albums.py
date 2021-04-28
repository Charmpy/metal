import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Album(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'albums'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    artistid = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey(
                                  "artists.id", ondelete='SET DEFAULT'),
                                 default=0
                                 )
    raiting = sqlalchemy.Column(sqlalchemy.Integer)
