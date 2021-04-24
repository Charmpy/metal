from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import make_response
from flask import jsonify
from forms.user import RegisterForm
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
    db_sess = db_session.create_session()

    # artist = Artist(name='Queen')
    # db_sess.add(artist)
    # artist = Artist(name='Metallica')
    # db_sess.add(artist)
    #
    # genre = Genre(name='Rock')
    # db_sess.add(genre)
    # genre = Genre(name='Metal')
    # db_sess.add(genre)

    # album = Album(title='Master of puppets', artistid=2, raiting=0)
    # db_sess.add(album)

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

# ##-----СПИСКИ----###


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


# ###-----ДЛЯ ЖАНРА-----###



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
