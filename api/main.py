from flask import Flask
from data import db_session
from flask_restful import Api
from resources import albums_resources


app = Flask(__name__)
api = Api(app)

api.add_resource(albums_resources.AlbumListResource, '/api/albums')
api.add_resource(albums_resources.AlbumResource, '/api/albums/<int:album_id>')

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/music_db.sqlite")
    app.run()


if __name__ == '__main__':
    main()
