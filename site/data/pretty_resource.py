from flask_restful import Resource
from flask import jsonify
from . import db_session
from .genres import Genre
from .artists import Artist
from .albums import Album
from .tracks import Track


class PrettyResource(Resource):
    def get(self, param):
        db_sess = db_session.create_session()
        if param == 'albums':
            albums = db_sess.query(Album).all()
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
            return jsonify(out)

        elif param == 'genres':
            genres = db_sess.query(Genre).all()
            out = []
            for i in genres:
                out.append({'genre': {'id': i.id, 'name': i.name}})
            return jsonify(out)

        elif param == 'artists':
            artists = db_sess.query(Artist).all()
            out = []
            for i in artists:
                k = len(
                    db_sess.query(Album).filter(Album.artistid == i.id).all())
                out.append({'artist': i.to_dict(
                            only=(
                                'id', 'name'
                            )), 'albums': k})
            return out

        elif param == 'tracks':
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
        return {'message': 'Bad param'}
