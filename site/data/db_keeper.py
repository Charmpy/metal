from . import db_session
from .genres import Genre
from .artists import Artist
from .albums import Album
from .tracks import Track
from .customers import Customer
from requests import get


class DataKeeper:
    def globon(self):
        db_session.global_init("db/music_db.sqlite")

    def get_pretty_albums_list(self):
        db_sess = db_session.create_session()
        albums = db_sess.query(Album).filter(Album.id > 0).all()
        out = []
        for i in albums:
            tracks = db_sess.query(Track).filter(
                Track.albumid == i.id).all()
            artist = db_sess.query(Artist).filter(
                Artist.id == i.artistid).first().name
            duration = sum(map(lambda x: x.seconds, tracks))
            out.append(
                {'album': i.to_dict(
                    only=(
                        'id', 'title'
                    )), 'duration': duration // 60,
                    'artist': artist}
            )
        return out

    def get_genres(self):
        db_sess = db_session.create_session()
        genres = db_sess.query(Genre).filter(Genre.id > 0).all()
        out = []
        for i in genres:
            out.append({'genre': {'id': i.id, 'name': i.name}})
        return out

    def get_pretty_artists_list(self):
        db_sess = db_session.create_session()
        artists = db_sess.query(Artist).filter(Artist.id > 0).all()
        out = []
        for i in artists:
            k = len(
                db_sess.query(Album).filter(Album.artistid == i.id).all())
            out.append({'artist': i.to_dict(
                only=(
                    'id', 'name'
                )), 'albums': k})
        return out

    def get_pretty_tracks_list(self):
        db_sess = db_session.create_session()
        tracks = db_sess.query(Track).all()
        out = []
        for i in tracks:
            artist = db_sess.query(Artist).filter(
                Artist.id == db_sess.query(Album).filter(
                    Album.id == i.albumid
                ).first().artistid
            ).first()
            album = db_sess.query(Album).filter(
                Album.id == i.albumid).first()
            out.append({'track': i.to_dict(
                only=(
                    'id', 'name', 'seconds'
                )),
                'album': album.to_dict(
                    only=(
                        'id', 'title'
                    )),
                'artist': artist.to_dict(
                    only=(
                        'id', 'name'
                    ))})
        return out

    ###########################
    # ###-----ДЛЯ ЖАНРА-----###
    ###########################

    def add_genre(self, name):
        db_sess = db_session.create_session()
        genre = Genre()
        genre.name = name
        db_sess.add(genre)
        db_sess.commit()

    def edit_genre_ac(self, id):
        db_sess = db_session.create_session()
        genre = db_sess.query(Genre).filter(
            Genre.id == id, Genre.id > 0).first()
        if genre:
            return genre
        return False

    def edit_genre(self, id, name):
        db_sess = db_session.create_session()
        genre = db_sess.query(Genre).filter(
            Genre.id == id, Genre.id > 0
        ).first()
        if genre:
            genre.name = name
            db_sess.commit()
            return True
        return False

    def get_genre(self, id):
        db_sess = db_session.create_session()
        genre = db_sess.query(Genre).filter(
            Genre.id == id, Genre.id > 0
        ).first()
        if genre:
            return {'genre': genre.to_dict(
                only=(
                    'id', 'name'
                ))}
        return False

    def delete_genre(self, id):
        db_sess = db_session.create_session()
        genre = db_sess.query(Genre).filter(
            Genre.id == id, Genre.id > 0
        ).first()
        if genre:
            db_sess.delete(genre)
            db_sess.commit()
            return True
        return False

    #############################
    # ###-----ДЛЯ АРТИСТОВ----###
    #############################
    def get_artist(self, id):
        db_sess = db_session.create_session()
        artist = db_sess.query(Artist).filter(
            Artist.id == id, Artist.id > 0
        ).first()
        if artist:
            return {'artist': artist.to_dict(
                only=(
                    'id', 'name'
                ))}
        return False

    def add_artist(self, name):
        db_sess = db_session.create_session()
        artist = Artist()
        artist.name = name
        db_sess.add(artist)
        db_sess.commit()

    def edit_artist_ac(self, id):
        db_sess = db_session.create_session()
        artist = db_sess.query(Artist).filter(Artist.id == id).first()
        if artist:
            return artist
        return False

    def edit_artist(self, id, name):
        db_sess = db_session.create_session()
        artist = db_sess.query(Artist).filter(
            Artist.id == id, Artist.id > 0
        ).first()
        if artist:
            artist.name = name
            db_sess.commit()
            return True
        return False

    def delete_artist(self, id):
        db_sess = db_session.create_session()
        artist = db_sess.query(Artist).filter(
            Artist.id == id, Artist.id > 0
        ).first()
        if artist:
            db_sess.delete(artist)
            db_sess.commit()
            return True
        return False

    def get_artists(self):
        db_sess = db_session.create_session()
        artists = db_sess.query(Artist).filter(Artist.id > 0).all()
        return [{'artist': i.to_dict(
                only=(
                    'id', 'name'
                ))} for i in artists]

    #############################
    # ###-----ДЛЯ АЛЬБОМОВ----###
    #############################

    def get_artists_choices(self):
        db_sess = db_session.create_session()
        artist = db_sess.query(Artist).filter(Artist.id > 0).all()
        choices = []
        for i in artist:
            choices.append((i.id, i.name))
        return choices

    def add_album(self, title, artistid):
        db_sess = db_session.create_session()
        album = Album()
        album.title = title
        album.artistid = artistid
        db_sess.add(album)
        db_sess.commit()

    def edit_album_ac(self, id):
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(Album.id == id).first()
        if album:
            return album
        return False

    def edit_album(self, id, title, artistid):
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(
            Album.id == id, Album.id > 0
        ).first()
        if album:
            album.title = title
            album.artistid = artistid
            db_sess.commit()
            return True
        return False

    def delete_album(self, id):
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(
            Album.id == id, Album.id > 0
        ).first()
        if album:
            db_sess.delete(album)
            db_sess.commit()
            return True
        return False

    def get_album(self, id):
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(
            Album.id == id, Album.id > 0
        ).first()
        if album:
            return {'album': album.to_dict(
                only=(
                    'id', 'title', 'artistid'
                ))}
        return False

    def get_albums(self):
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(Album.id > 0).all()
        return [{'album': i.to_dict(
            only=(
                'id', 'title', 'artistid'
            ))} for i in album]

    ######################
    # ###----ТРЕКИ-----###
    ######################

    def get_tracks(self):
        db_sess = db_session.create_session()
        track = db_sess.query(Track).all()
        if track:
            return [{'track': i.to_dict(
                only=(
                    'id', 'name', 'genreid', 'albumid', 'seconds'
                ))} for i in track]
        return False

    def get_track(self, id):
        db_sess = db_session.create_session()
        track = db_sess.query(Track).filter(Track.id == id).first()
        if track:
            return {'track': track.to_dict(
                only=(
                    'id', 'name', 'genreid', 'albumid', 'seconds'
                ))}
        return False

    def get_albums_choices(self):
        db_sess = db_session.create_session()
        albums = db_sess.query(Album).filter(Album.id > 0).all()
        choices = []
        for i in albums:
            choices.append((i.id, i.title))
        return choices

    def get_genres_choices(self):
        db_sess = db_session.create_session()
        genre = db_sess.query(Genre).filter(Genre.id > 0).all()
        choices = []
        for i in genre:
            choices.append((i.id, i.name))
        return choices

    def add_track(self, name, albumid, genreid, seconds):
        db_sess = db_session.create_session()
        track = Track()
        track.name = name
        track.albumid = albumid
        track.genreid = genreid
        track.seconds = seconds
        db_sess.add(track)
        db_sess.commit()

    def edit_track_ac(self, id):
        db_sess = db_session.create_session()
        track = db_sess.query(Track).filter(Track.id == id).first()
        if track:
            return track
        return False

    def edit_track(self, id, name, albumid, genreid, seconds):
        db_sess = db_session.create_session()
        track = db_sess.query(Track).filter(Track.id == id).first()
        if track:
            track.name = name
            track.albumid = albumid
            track.genreid = genreid
            track.seconds = seconds
            db_sess.commit()
            return True
        return False

    def delete_track(self, id):
        db_sess = db_session.create_session()
        track = db_sess.query(Track).filter(Track.id == id).first()
        if track:
            db_sess.delete(track)
            db_sess.commit()
            return True
        return False

    def get_pretty_album_info(self, id):
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(
            Album.id == id, Album.id > 0
        ).first()
        if album:
            tracks = db_sess.query(Track).filter(Track.albumid == id).all()
            artist = db_sess.query(Artist).filter(
            Artist.id == album.artistid).first()
            return {'album': album, 'tracks': tracks, 'artist': artist}
        return False

    ################
    # ###--------###
    ################

    def login_user(self, email, password):
        db_sess = db_session.create_session()
        user = db_sess.query(Customer).filter(
            Customer.email == email).first()
        if user and user.check_password(password):
            return user
        else:
            return False

    def register(self, email, password, name, surname):
        db_sess = db_session.create_session()
        if db_sess.query(Customer).filter(Customer.email == email).first():
            return True
        user = Customer(
            name=name,
            surname=surname,
            email=email,
        )
        user.set_password(password)
        db_sess.add(user)
        db_sess.commit()
        return False

    def load_user(self, id):
        db_sess = db_session.create_session()
        return db_sess.query(Customer).get(id)