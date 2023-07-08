from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import *
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import func
import os

IMAGE_FOLDER = os.path.join('../Audio_Streaming_Platform/static', 'Image')

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ninninu'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Internet10@localhost:5432/Audio_Streaming_Platform"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


db = SQLAlchemy(app)


@login_manager.user_loader
def load_user(id_users):
    user = db.session.query(Users).filter(Users.id_users == id_users).first()

    return user


class Users(UserMixin, db.Model):
    id_users = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    sex = db.Column(db.String)
    mail = db.Column(db.String, unique=True)
    pwd = db.Column(db.String)
    birth_date = db.Column(db.Date)
    authenticated = db.Column(db.Boolean, default=False)
    image = db.Column(db.String)

    def __init__(self, name, surname, sex, mail, pwd, birth_date, image):
        self.name = name
        self.surname = surname
        self.sex = sex
        self.mail = mail
        self.pwd = pwd
        self.birth_date = birth_date
        self.image = image

    def get_id(self):
        return self.id_users

    def is_artist(self):
        art = db.session.query(Artists).filter(Artists.id_artists == self.id_users)
        count = 0
        for a in art:
            count = count + 1

        if count >= 1:
            return True
        return False


class Artists(db.Model):
    id_artists = db.Column(db.Integer, db.ForeignKey('users.id_users'), primary_key=True, )
    art_name = db.Column(db.String)
    label = db.Column(db.String)

    def __init__(self, id_artists, art_name, label):
        self.id_artists = id_artists
        self.art_name = art_name
        self.label = label


class Songs(db.Model):
    id_songs = db.Column(db.Integer, primary_key=True)
    id_artist = db.Column(db.Integer, db.ForeignKey('artists.id_artists'))
    title = db.Column(db.String)
    length = db.Column(db.Integer)
    date_pub = db.Column(db.Date)
    type = db.Column(db.String)
    image = db.Column(db.String)

    def __init__(self, id_artists, title, length, date_pub, type, image):
        self.id_artist = id_artists
        self.title = title
        self.length = length
        self.date_pub = date_pub
        self.type = type
        self.image = image


class Playlist(db.Model):
    id_playlist = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    date_creation = db.Column(db.Date)
    private = db.Column(db.Boolean, default=False)

    def __init__(self, id_playlist, name, description, date_creation, private):
        self.id_playlist = id_playlist
        self.name = name
        self.description = description
        self.date_creation = date_creation
        self.private = private


class Album(db.Model):
    id_album = db.Column(db.Integer, primary_key=True)
    id_artist = db.Column(db.Integer, db.ForeignKey('artists.id_artists'))
    date_pub = db.Column(db.Date)
    title = db.Column(db.String)
    image = db.Column(db.String)

    def __init__(self, id_artist, date_pub, title, image):
        self.id_artist = id_artist
        self.date_pub = date_pub
        self.title = title
        self.image = image


class PlaylistSongs(db.Model):
    id_songs = db.Column(db.Integer, db.ForeignKey('songs.id_songs'), primary_key=True)
    id_playlist = db.Column(db.Integer, db.ForeignKey('playlist.id_playlist'), primary_key=True)

    def __init__(self, id_songs, id_playlist):
        self.id_songs = id_songs
        self.id_playlist = id_playlist


class PlaylistUsers(db.Model):
    id_users = db.Column(db.Integer, db.ForeignKey('users.id_users'), primary_key=True)
    id_playlist = db.Column(db.Integer, db.ForeignKey('playlist.id_playlist'), primary_key=True)
    count_song = db.Column(db.Integer)

    def __init__(self, id_users, id_playlist, count_song):
        self.id_users = id_users
        self.id_playlist = id_playlist
        count_song = count_song


class SongsAlbum(db.Model):
    id_album = db.Column(db.Integer, db.ForeignKey('album.id_album'), primary_key=True)
    id_songs = db.Column(db.Integer, db.ForeignKey('songs.id_songs'), primary_key=True)

    def __init__(self, id_album, id_songs):
        self.id_album = id_album
        self.id_songs = id_songs


class SongsListened(db.Model):
    id_songs = db.Column(db.Integer, db.ForeignKey('songs.id_songs'), primary_key=True)
    id_users = db.Column(db.Integer, db.ForeignKey('users.id_users'), primary_key=True)
    num_times = db.Column(db.Integer)
    date_list = db.Column(db.Date)

    def __init__(self, id_songs, id_users, num_times, date_list):
        self.id_songs = id_songs
        self.id_users = id_users
        self.num_times = num_times
        self.date_list = date_list


db.create_all()

