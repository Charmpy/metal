from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import make_response, request
from flask import jsonify, abort
from forms.user import RegisterForm
from forms.genresform import GenresForm
from forms.artistsform import ArtistsForm
from forms.tracksform import TracksForm
from forms.albumsform import AlbumsForm
from data.loginform import LoginForm
from data.db_keeper import DataKeeper
from data.pretty_resource import PrettyResource
from data.genres_resource import GenresResource, GenresListResource
from data.artists_resource import ArtistsListResource, ArtistsResource
from data.albums_resource import AlbumsListResource, AlbumsResource
from data.tracks_resource import TracksListResource, TracksResource
from flask_restful import abort, Api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

keeper = DataKeeper()

api = Api(app)

api.add_resource(PrettyResource, '/api/pretty/<param>')

api.add_resource(GenresResource, '/api/genres/<int:genre_id>')
api.add_resource(GenresListResource, '/api/genres')

api.add_resource(ArtistsResource, '/api/artists/<int:artist_id>')
api.add_resource(ArtistsListResource, '/api/artists')

api.add_resource(AlbumsResource, '/api/albums/<int:album_id>')
api.add_resource(AlbumsListResource, '/api/albums')

api.add_resource(TracksResource, '/api/tracks/<int:track_id>')
api.add_resource(TracksListResource, '/api/tracks')


def main():
    keeper.globon()
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/")
def index():
    return render_template("index.html", title='Hall')


######################
# ##-----СПИСКИ----###
######################
@app.route("/albums_list")
def albums_list():
    info = keeper.get_pretty_albums_list()
    return render_template("albums.html", title='Hall', lst=info)


@app.route("/genres_list")
def genres_list():
    genres = keeper.get_genres()
    return render_template("genres.html", title='Hall', genres=genres)


@app.route("/artists_list")
def artists_list():
    out = keeper.get_pretty_artists_list()
    return render_template("artists.html", title='Hall', artists=out)


@app.route("/tracks_list")
def tracks_list():
    out = keeper.get_pretty_tracks_list()
    return render_template("tracks.html", title='Hall', tracks=out)


###########################
# ###-----ДЛЯ ЖАНРА-----###
###########################
@app.route('/genres',  methods=['GET', 'POST'])
@login_required
def add_genre():
    form = GenresForm()
    if form.validate_on_submit():
        keeper.add_genre(form.name.data)
        return redirect('/genres_list')
    return render_template('genres_form.html', title='Genre adding',
                           form=form)


@app.route('/genres/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_genre(id):
    form = GenresForm()
    if request.method == "GET":
        genre = keeper.edit_genre_ac(id)
        if genre:
            form.name.data = genre.name
        else:
            abort(404)
    if form.validate_on_submit():
        genre = keeper.edit_genre(id, form.name.data)
        if genre:
            return redirect('/genres_list')
        else:
            abort(404)
    return render_template('genres_form.html',
                           title='Genre fix',
                           form=form
                           )


@app.route('/genres_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def genre_delete(id):
    genre = keeper.delete_genre(id)
    if not genre:
        abort(404)
    return redirect('/genres_list')


#############################
# ###-----ДЛЯ АРТИСТОВ----###
#############################
@app.route('/artists',  methods=['GET', 'POST'])
@login_required
def add_artist():
    form = ArtistsForm()
    if form.validate_on_submit():
        keeper.add_artist(form.name.data)
        return redirect('/artists_list')
    return render_template('artists_form.html', title='Artist adding',
                           form=form)


@app.route('/artists/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_artist(id):
    form = ArtistsForm()
    if request.method == "GET":
        artist = keeper.edit_artist_ac(id)
        if artist:
            form.name.data = artist.name
        else:
            abort(404)
    if form.validate_on_submit():
        artist = keeper.edit_artist(id, form.name.data)
        if artist:
            return redirect('/artists_list')
        else:
            abort(404)
    return render_template('artists_form.html',
                           title='Artist fix',
                           form=form
                           )


@app.route('/artists_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def artist_delete(id):
    artist = keeper.delete_artist(id)
    if not artist:
        abort(404)
    return redirect('/artists_list')


#############################
# ###-----ДЛЯ АЛЬБОМОВ----###
#############################
@app.route('/albums',  methods=['GET', 'POST'])
@login_required
def add_albums():
    form = AlbumsForm()
    form.artistid.choices = keeper.get_artists_choices()
    if form.validate_on_submit():
        keeper.add_album(form.title.data, form.artistid.data)
        return redirect('/albums_list')
    return render_template('albums_form.html', title='Artist adding',
                           form=form)


@app.route('/albums/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_albums(id):
    form = AlbumsForm()
    form.artistid.choices = keeper.get_artists_choices()

    if request.method == "GET":
        album = keeper.edit_album_ac(id)
        if album:
            form.title.data = album.title
            form.artistid.data = album.artistid
        else:
            abort(404)
    if form.validate_on_submit():
        album = keeper.edit_album(id, form.title.data, form.artistid.data)
        if album:
            return redirect('/albums_list')
        else:
            abort(404)
    return render_template('albums_form.html',
                           title='Album fix',
                           form=form
                           )


@app.route('/albums_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def albums_delete(id):
    album = keeper.delete_album(id)
    if not album:
        abort(404)
    return redirect('/albums_list')


######################
# ###----ТРЕКИ-----###
######################
@app.route('/tracks',  methods=['GET', 'POST'])
@login_required
def add_tracks():
    form = TracksForm()

    form.albumid.choices = keeper.get_albums_choices()
    form.genreid.choices = keeper.get_genres_choices()

    if form.validate_on_submit():
        keeper.add_track(
            form.name.data, form.albumid.data,
            form.genreid.data, form.seconds.data
        )
        return redirect('/tracks_list')
    return render_template('tracks_form.html', title='Artist adding',
                           form=form)


@app.route('/tracks/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tracks(id):
    form = TracksForm()

    form.albumid.choices = keeper.get_albums_choices()
    form.genreid.choices = keeper.get_genres_choices()

    if request.method == "GET":
        track = keeper.edit_track_ac(id)
        if track:
            form.name.data = track.name
            form.albumid.data = track.albumid
            form.genreid.data = track.genreid
            form.seconds.data = track.seconds
        else:
            abort(404)
    if form.validate_on_submit():
        track = keeper.edit_track(
            id,
            form.name.data, form.albumid.data,
            form.genreid.data, form.seconds.data
        )
        if track:
            return redirect('/tracks_list')
        else:
            abort(404)
    return render_template('tracks_form.html',
                           title='Track fix',
                           form=form
                           )


@app.route('/tracks_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def track_delete(id):
    track = keeper.delete_track(id)
    if not track:
        abort(404)
    return redirect('/tracks_list')

################
# ###--------###
################


@app.route('/album_info/<int:id>', methods=['GET', 'POST'])
def album_info(id):
    album = keeper.get_pretty_album_info(id)
    if not album:
        abort(404)
    return render_template(
        'albums_info.html', title=album["album"].title, info=album
    )


################
# ###--------###
################

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = keeper.login_user(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        new_user = keeper.register(
            form.email.data, form.password.data, form.name.data, form.surname.data
        )
        if new_user:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    return keeper.load_user(user_id)


if __name__ == '__main__':
    main()
