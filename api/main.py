from flask import Flask
from data import db_session
from flask_restful import Api
from resources import albums_resources, artists_resources, genres_resource
from data.customers import Customer
from data.genres import Genre
from data.artists import Artist
from data.albums import Album
from data.tracks import Track


app = Flask(__name__)
api = Api(app)

# жанры
api.add_resource(genres_resource.GenreListResource, '/api/genres')
api.add_resource(
    genres_resource.GenreResource, '/api/genres/<int:genre_id>'
)

# Альбомы
api.add_resource(albums_resources.AlbumListResource, '/api/albums')
api.add_resource(albums_resources.AlbumResource, '/api/albums/<int:album_id>')

# Исполнители
api.add_resource(artists_resources.ArtistListResource, '/api/artists')
api.add_resource(
    artists_resources.ArtistResource, '/api/artists/<int:artist_id>'
)



app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



def main():
    db_session.global_init("db/music_db.sqlite")
    app.run()


if __name__ == '__main__':
    main()
