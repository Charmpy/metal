from flask_restful import reqparse, abort, Resource
from data import db_session
from api.data.genres import Genre
from flask import jsonify


class GenreResource(Resource):
    def get(self, genre_id):
        abort_if_genre_not_found(genre_id)
        session = db_session.create_session()
        genre = session.query(Genre).get(genre_id)

        return jsonify({'genre': genre.to_dict(
            only=(
                'id', 'name'
            ))})

    def delete(self, genre_id):
        abort_if_genre_not_found(genre_id)
        session = db_session.create_session()
        genre = session.query(Genre).get(genre_id)
        session.delete(genre)
        session.commit()
        return jsonify({'success': 'OK'})


class GenreListResource(Resource):
    def get(self):
        session = db_session.create_session()
        artists = session.query(Genre).all()
        return jsonify({'genre': [item.to_dict(
            only=(
                'id', 'name'
            )) for item in artists]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        session = db_session.create_session()
        genre = Genre(
            name=args["name"],
        )
        session.add(genre)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_genre_not_found(genre_id):
    session = db_session.create_session()
    genre = session.query(Genre).get(genre_id)
    if not genre:
        abort(404, message=f"Genre {genre_id} not found")