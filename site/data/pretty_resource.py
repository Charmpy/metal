from flask_restful import Resource
from flask import jsonify
from .db_keeper import DataKeeper


class PrettyResource(Resource):
    data = DataKeeper()

    def get(self, param):
        if param == 'albums':
            out = self.data.get_pretty_albums_list()
            return jsonify(out)

        elif param == 'genres':
            out = self.data.get_genres()
            return jsonify(out)

        elif param == 'artists':
            out = self.data.get_pretty_artists_list()
            return jsonify(out)

        elif param == 'tracks':
            out = self.data.get_pretty_tracks_list()
            return jsonify(out)
        return {'message': 'Bad param'}

