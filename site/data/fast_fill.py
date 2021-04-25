from . import db_session
from .genres import Genre
from .artists import Artist
from .albums import Album
from .tracks import Track


db_session.global_init("music_db.sqlite")
db_sess = db_session.create_session()

artist = Artist(name='Queen')
db_sess.add(artist)
artist = Artist(name='Metallica')
db_sess.add(artist)

genre = Genre(name='Rock')
db_sess.add(genre)
genre = Genre(name='Metal')
db_sess.add(genre)

album = Album(title='Master of puppets', artistid=2, raiting=0)
db_sess.add(album)

for name, long in [
    ['Battery', 312],
    ['Master Of Puppets', 515],
    ['The Thing That Should Not Be', 396],
    ['Welcome Home (Sanitarium)', 387],
    ['Disposable Heroes', 496],
    ['Leper Messiah', 339],
    ['Orion', 507],
    ['Damage, Inc.', 332]
]:
    db_sess.add(Track(name=name, albumid=1, genreid=2, seconds=long))

db_sess.commit()
