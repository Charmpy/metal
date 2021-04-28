from flask_restful import reqparse, Resource
from .db_keeper import DataKeeper
from flask import jsonify


class TracksResource(Resource):
    data = DataKeeper()

    def get(self, track_id):
        out = self.data.get_track(track_id)
        if bool(out):
            return jsonify(out)
        return jsonify({'message': 'Wrong id'})

    def delete(self, track_id):
        out = self.data.delete_track(track_id)
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})

    def put(self, track_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('albumid', required=True)
        parser.add_argument('genreid', required=True)
        parser.add_argument('seconds', required=True)
        args = parser.parse_args()
        out = self.data.edit_track(
            track_id,
            args['name'],
            args['albumid'],
            args['genreid'],
            args['seconds'],
        )
        if bool(out):
            return jsonify({'success': 'OK'})
        return jsonify({'message': 'Wrong id'})


class TracksListResource(Resource):
    data = DataKeeper()

    def get(self):
        out = self.data.get_tracks()
        return jsonify(out)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('albumid', required=True)
        parser.add_argument('genreid', required=True)
        parser.add_argument('seconds', required=True)
        args = parser.parse_args()
        self.data.add_track(
            args['name'],
            args['albumid'],
            args['genreid'],
            args['seconds'],
        )
        return jsonify({'success': 'OK'})
