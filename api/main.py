from flask import Flask
from data import db_session
from flask_restful import Api
from resources import customers_resources, artists_resources


app = Flask(__name__)
api = Api(app)

api.add_resource(customers_resources.CustomerListResource, '/api/add_customer')
api.add_resource(customers_resources.CustomerResource, '/api/customers/<int:customer_id>')

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
