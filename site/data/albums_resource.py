from flask_restful import reqparse, Resource
from .db_keeper import DataKeeper
from flask import jsonify


class AlbumsResource(Resource):
    data = DataKeeper()

    def get(self, album_id):
        out = self.data.get_album(album_id)
        if bool(out):
            return jsonify(out)
        return jsonify({'message': 'Wrong id'})

    def delete(self, album_id):
        out = self.data.delete_album(album_id)
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})

    def put(self, album_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('artistid', required=True)
        args = parser.parse_args()
        out = self.data.edit_album(album_id, args['title'], args['artistid'])
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})


class AlbumsListResource(Resource):
    data = DataKeeper()

    def get(self):
        out = self.data.get_albums()
        return jsonify(out)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('artistid', required=True)
        args = parser.parse_args()
        self.data.add_album(args['title'], args['artistid'])
        return jsonify({'success': 'OK'})
