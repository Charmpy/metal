from flask_restful import reqparse, Resource
from .db_keeper import DataKeeper
from flask import jsonify


class ArtistsResource(Resource):
    data = DataKeeper()

    def get(self, artist_id):
        out = self.data.get_artist(artist_id)
        if bool(out):
            return jsonify(out)
        return jsonify({'message': 'Wrong id'})

    def delete(self, artist_id):
        out = self.data.delete_artist(artist_id)
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})

    def put(self, artist_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        out = self.data.edit_artist(artist_id, args['name'])
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})


class ArtistsListResource(Resource):
    data = DataKeeper()

    def get(self):
        out = self.data.get_artists()
        return jsonify(out)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        self.data.add_artist(args['name'])
        return jsonify({'success': 'OK'})
