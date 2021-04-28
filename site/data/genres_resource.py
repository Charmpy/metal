from flask_restful import reqparse, Resource
from .db_keeper import DataKeeper
from flask import jsonify


class GenresResource(Resource):
    data = DataKeeper()

    def get(self, genre_id):
        out = self.data.get_genre(genre_id)
        if bool(out):
            return jsonify(out)

        return jsonify({'message': 'Wrong id'})

    def delete(self, genre_id):
        out = self.data.delete_genre(genre_id)
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})

    def put(self, genre_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        out = self.data.edit_genre(genre_id, args['name'])
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})


class GenresListResource(Resource):
    data = DataKeeper()

    def get(self):
        out = self.data.get_genres()
        return jsonify(out)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        self.data.add_genre(args['name'])
        return jsonify({'success': 'OK'})
