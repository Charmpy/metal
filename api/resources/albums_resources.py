from flask_restful import reqparse, abort, Resource
from data import db_session
from api.data.albums import Album
from flask import jsonify


class AlbumResource(Resource):
    def get(self, album_id):
        abort_if_album_not_found(album_id)
        session = db_session.create_session()
        album = session.query(Album).get(album_id)

        return jsonify({'album': album.to_dict(
            only=(
                'id', 'title', 'artistid', 'raiting'
            ))})

    def delete(self, album_id):
        abort_if_album_not_found(album_id)
        session = db_session.create_session()
        album = session.query(Album).get(album_id)
        session.delete(album)
        session.commit()
        return jsonify({'success': 'OK'})


class AlbumListResource(Resource):
    def get(self):
        session = db_session.create_session()
        albums = session.query(Album).all()
        return jsonify({'albums': [item.to_dict(
            only=(
                'id', 'title', 'artistid'
            )) for item in albums]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('artistid', required=True, type=int)
        args = parser.parse_args()
        session = db_session.create_session()
        album = Album(
            title=args["title"],
            artistid=args["artistid"],
            raiting=0
        )
        session.add(album)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_album_not_found(jobs_id):
    session = db_session.create_session()
    news = session.query(Album).get(jobs_id)
    if not news:
        abort(404, message=f"Album {jobs_id} not found")
