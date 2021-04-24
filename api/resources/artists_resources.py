from flask_restful import reqparse, abort, Resource
from data import db_session
from api.data.artists import Artist
from flask import jsonify


class ArtistResource(Resource):
    def get(self, artist_id):
        abort_if_artist_not_found(artist_id)
        session = db_session.create_session()
        artist = session.query(Artist).get(artist_id)

        return jsonify({'artist': artist.to_dict(
            only=(
                'id', 'name'
            ))})

    def delete(self, artist_id):
        abort_if_artist_not_found(artist_id)
        session = db_session.create_session()
        album = session.query(Artist).get(artist_id)
        session.delete(album)
        session.commit()
        return jsonify({'success': 'OK'})


class ArtistListResource(Resource):
    def get(self):
        session = db_session.create_session()
        artists = session.query(Artist).all()
        return jsonify({'artist': [item.to_dict(
            only=(
                'id', 'name'
            )) for item in artists]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        session = db_session.create_session()
        album = Artist(
            name=args["name"],
        )
        session.add(album)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_artist_not_found(artist_id):
    session = db_session.create_session()
    news = session.query(Artist).get(artist_id)
    if not news:
        abort(404, message=f"Artist {artist_id} not found")

