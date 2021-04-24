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
from data import db_session
from data.customers import Customer
from data.genres import Genre
from data.artists import Artist
from data.albums import Album
from data.tracks import Track

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/music_db.sqlite")
    # db_sess = db_session.create_session()
    #
    # artist = Artist(name='Queen')
    # db_sess.add(artist)
    # artist = Artist(name='Metallica')
    # db_sess.add(artist)
    #
    # genre = Genre(name='Rock')
    # db_sess.add(genre)
    # genre = Genre(name='Metal')
    # db_sess.add(genre)
    #
    # album = Album(title='Master of puppets', artistid=2, raiting=0)
    # db_sess.add(album)
    #
    # for name, long in [
    #     ['Battery', 312],
    #     ['Master Of Puppets', 515],
    #     ['The Thing That Should Not Be', 396],
    #     ['Welcome Home (Sanitarium)', 387],
    #     ['Disposable Heroes', 496],
    #     ['Leper Messiah', 339],
    #     ['Orion', 507],
    #     ['Damage, Inc.', 332]
    # ]:
    #     db_sess.add(Track(name=name, albumid=1, genreid=2, seconds=long))
    #
    # db_sess.commit()
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
    db_sess = db_session.create_session()
    albums = db_sess.query(Album).all()
    out = []
    for i in albums:
        tracks = db_sess.query(Track).filter(Track.albumid == i.id).all()
        artist = db_sess.query(Artist).filter(
            Artist.id == i.artistid).first().name
        duration = sum(map(lambda x: x.seconds, tracks))
        print(duration)
        out.append({'album': i, 'duration': duration // 60, 'artist': artist})
    return render_template("albums.html", title='Hall', lst=out)


@app.route("/genres_list")
def genres_list():
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    print(genres)
    return render_template("genres.html", title='Hall', genres=genres)


@app.route("/artists_list")
def artists_list():
    db_sess = db_session.create_session()
    artists = db_sess.query(Artist).all()
    out = []
    for i in artists:
        k = len(db_sess.query(Album).filter(Album.artistid == i.id).all())
        out.append({'artist': i, 'albums': k})
    return render_template("artists.html", title='Hall', artists=out)


@app.route("/tracks_list")
def tracks_list():
    db_sess = db_session.create_session()
    tracks = db_sess.query(Track).all()
    out = []
    for i in tracks:
        artist = db_sess.query(Artist).filter(
            Artist.id == db_sess.query(Album).filter(Album.id == i.albumid
                                                     ).first().artistid
        ).first()
        album = db_sess.query(Album).filter(Album.id == i.albumid).first()
        out.append({'track': i, 'album': album, 'artist': artist})
    print(out)
    return render_template("tracks.html", title='Hall', tracks=out)

###########################
# ###-----ДЛЯ ЖАНРА-----###
###########################
@app.route('/genres',  methods=['GET', 'POST'])
@login_required
def add_genre():
    form = GenresForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        genre = Genre()
        genre.name = form.name.data
        db_sess.add(genre)
        db_sess.commit()
        return redirect('/genres_list')
    return render_template('genres_form.html', title='Genre adding',
                           form=form)


@app.route('/genres/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_genre(id):
    form = GenresForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        genre = db_sess.query(Genre).filter(Genre.id == id).first()
        if genre:
            form.name.data = genre.name
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        genre = db_sess.query(Genre).filter(Genre.id == id).first()
        if genre:
            genre.name = form.name.data
            db_sess.commit()
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
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).filter(Genre.id == id).first()
    if genre:
        db_sess.delete(genre)
        db_sess.commit()
    else:
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
        db_sess = db_session.create_session()
        artist = Artist()
        artist.name = form.name.data
        db_sess.add(artist)
        db_sess.commit()
        return redirect('/artists_list')
    return render_template('artists_form.html', title='Artist adding',
                           form=form)


@app.route('/artists/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_artist(id):
    form = ArtistsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        artist = db_sess.query(Artist).filter(Artist.id == id).first()
        if artist:
            form.name.data = artist.name
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        artist = db_sess.query(Artist).filter(Artist.id == id).first()
        if artist:
            artist.name = form.name.data
            db_sess.commit()
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
    db_sess = db_session.create_session()
    artist = db_sess.query(Artist).filter(Artist.id == id).first()
    if artist:
        db_sess.delete(artist)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/artists_list')

#############################
# ###-----ДЛЯ АЛЬБОМОВ----###
#############################
@app.route('/albums',  methods=['GET', 'POST'])
@login_required
def add_albums():
    db_sess = db_session.create_session()
    artist = db_sess.query(Artist).all()
    choices = []
    for i in artist:
        choices.append((i.id, i.name))

    form = AlbumsForm()
    form.artistid.choices = choices

    if form.validate_on_submit():
        album = Album()
        album.title = form.title.data
        album.artistid = form.artistid.data
        db_sess.add(album)
        db_sess.commit()
        return redirect('/albums_list')
    return render_template('albums_form.html', title='Artist adding',
                           form=form)


@app.route('/albums/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_albums(id):
    db_sess = db_session.create_session()
    artist = db_sess.query(Artist).all()
    choices = []
    for i in artist:
        choices.append((i.id, i.name))

    form = AlbumsForm()
    form.artistid.choices = choices

    if request.method == "GET":
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(Album.id == id).first()
        if album:
            form.title.data = album.title
            form.artistid.data = album.artistid
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        album = db_sess.query(Album).filter(Album.id == id).first()
        if album:
            album.title = form.title.data
            album.artistid = form.artistid.data
            db_sess.commit()
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
    db_sess = db_session.create_session()
    album = db_sess.query(Album).filter(Album.id == id).first()
    if album:
        db_sess.delete(album)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/albums_list')


######################
# ###----ТРЕКИ-----###
######################
@app.route('/tracks',  methods=['GET', 'POST'])
@login_required
def add_tracks():
    db_sess = db_session.create_session()
    artist = db_sess.query(Album).all()
    art_choices = []
    for i in artist:
        art_choices.append((i.id, i.title))

    genre = db_sess.query(Genre).all()
    gen_choices = []
    for i in genre:
        gen_choices.append((i.id, i.name))

    form = TracksForm()
    form.albumid.choices = art_choices
    form.genreid.choices = gen_choices

    if form.validate_on_submit():
        track = Track()
        track.name = form.name.data
        track.albumid = form.albumid.data
        track.genreid = form.genreid.data
        track.seconds = form.seconds.data
        db_sess.add(track)
        db_sess.commit()
        return redirect('/tracks_list')
    return render_template('tracks_form.html', title='Artist adding',
                           form=form)


@app.route('/tracks/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tracks(id):
    db_sess = db_session.create_session()
    artist = db_sess.query(Album).all()
    art_choices = []
    for i in artist:
        art_choices.append((i.id, i.title))

    genre = db_sess.query(Genre).all()
    gen_choices = []
    for i in genre:
        gen_choices.append((i.id, i.name))

    form = TracksForm()
    form.albumid.choices = art_choices
    form.genreid.choices = gen_choices

    if request.method == "GET":
        db_sess = db_session.create_session()
        track = db_sess.query(Track).filter(Track.id == id).first()
        if track:
            form.name.data = track.name
            form.albumid.data = track.albumid
            form.genreid.data = track.genreid
            form.seconds.data = track.seconds
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        track = db_sess.query(Track).filter(Track.id == id).first()
        if track:
            track.name = form.name.data
            track.albumid = form.albumid.data
            track.genreid = form.genreid.data
            track.seconds = form.seconds.data
            db_sess.commit()
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
    db_sess = db_session.create_session()
    track = db_sess.query(Track).filter(Track.id == id).first()
    if track:
        db_sess.delete(track)
        db_sess.commit()
    else:
        abort(404)

    info = []
    return render_template('tracks_form.html',
                           title='Track fix',
                           info=info
                           )

################
# ###--------###
################


# @app.route('/album_info/<int:id>', methods=['GET', 'POST'])
# @login_required
# def track_delete(id):
#     db_sess = db_session.create_session()
#     track = db_sess.query(Track).filter(Track.id == id).first()
#     if track:
#         db_sess.delete(track)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/tracks_list')
#

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
        db_sess = db_session.create_session()
        user = db_sess.query(Customer).filter(Customer.email == form.email.data).first()
        if user and user.check_password(form.password.data):
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
        db_sess = db_session.create_session()
        if db_sess.query(Customer).filter(Customer.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = Customer(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Customer).get(user_id)


if __name__ == '__main__':
    main()
