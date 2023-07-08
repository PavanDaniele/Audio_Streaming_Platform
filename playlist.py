import json

from app import *
from auth import *
from stats import *
from stats import take_song, take_playlist, take_artist
from struttura_db import *
import datetime


def get_playlist():
    playlist = db.session.query(PlaylistUsers).filter(PlaylistUsers.id_users == current_user.id_users)
    play_list = []

    for play in playlist:

        tmp = []
        p = take_playlist(play.id_playlist)
        if p.name != 'Preferiti':
            tmp.append(p.name)
            tmp.append(play.count_song)
            tmp.append(play.id_playlist)
            play_list.append(tmp)

    return play_list


def is_love(id_playlist):

    playlist = db.session.query(Playlist).filter(Playlist.id_playlist == id_playlist).first()

    if playlist.name == 'Best Song of '+current_user.name:
        return True
    return False


def take_love():
    playlist_user = db.session.query(PlaylistUsers).filter(PlaylistUsers.id_users == current_user.id_users)
    for play in playlist_user:
        if is_love(play.id_playlist):
            return play
    return False


@app.route('/play_page', methods=['GET', 'POST'])
@login_required
def pl_page():
    play_list = get_playlist()
    playlist_img = os.path.join(app.config['UPLOAD_FOLDER'], "playlist_def.jpeg")
    playlist_logo_love = os.path.join(app.config['UPLOAD_FOLDER'], "heart.jpeg")
    play_love = take_love()

    return render_template('Playlist/playlist_list.html', playlist=play_list, user_image=upload_user_image(),
                           playlist_img=playlist_img, playlist_logo=playlist_logo_love, play_love=play_love)


def take_list_song(id_playlist):
    song = db.session.query(Songs)
    song_list = []
    for s in song:
        if not exits_song_playlist(id_playlist, s.id_songs):
            tmp = []
            tmp.append(s.id_songs)
            tmp.append(s.title)
            song_list.append(tmp)

    return song_list


def insert_song_playlist(id_song, playlist):
    list_song_play = []
    for play in playlist:
        if not exits_song_playlist(id_song, play.id_playlist):
            list_song_play.append(play)

    return list_song_play


@app.route('/playlist_page/<id_playlist>', methods=['GET', 'POST'])
@login_required
def playlist_page(id_playlist=None):

    playlist_list_song = db.session.query(PlaylistSongs).filter(PlaylistSongs.id_playlist == id_playlist)
    playlist = db.session.query(Playlist).filter(Playlist.id_playlist == id_playlist).first()
    all_playlist = db.session.query(Playlist).filter(Playlist.id_playlist != id_playlist)

    playlist_list = []
    count = 0

    for play in playlist_list_song:
        tmp = []
        count += 1
        song = take_song(play.id_songs)
        tmp.append(song)
        tmp.append("Image/"+song.image)
        tmp.append(take_artist(play.id_songs))
        tmp.append(str(datetime.timedelta(seconds=song.length)))
        tmp.append(count)
        tmp.append(insert_song_playlist(play.id_songs, all_playlist))
        playlist_list.append(tmp)

    if is_love(id_playlist):
        playlist_logo = "Image/heart.jpeg"
    else:
        playlist_logo = "Image/playlist_def.jpeg"

    return render_template('Playlist/playlists_interface.html', playlist=playlist, playlist_list_song=playlist_list,
                           playlist_logo="Image/playlist_def.jpeg",
                           user_image=upload_user_image())


@app.route('/playlist_prova/<int:id_playlist>', methods=['GET', 'POST'])
def playlist_prova(id_playlist):

    return render_template('Playlist/playlists_interface.html')


def count_id_playlist():
    return db.session.query(func.max(Playlist.id_playlist)).first()


def exits_song_playlist(id_song, id_playlist):

    song = db.session.query(PlaylistSongs).filter(PlaylistSongs.id_playlist == id_playlist)

    for s in song:
        if s.id_songs == id_song:
            return True

    return False


@app.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    if request.method == 'POST':
        lol = count_id_playlist()

        id_playlist = db.session.query(Playlist).count() + 1

        name = request.form['name']
        private = request.form['type']
        description = request.form['description']
        date_creation = date.today()

        if private == "True":
            playlist = Playlist(id_playlist, name, description, date_creation, True)
        else:
            playlist = Playlist(id_playlist, name, description, date_creation, False)

        db.session.add(playlist)
        db.session.commit()

        playlist_user = PlaylistUsers(current_user.id_users, id_playlist, 0)

        db.session.add(playlist_user)
        db.session.commit()

        return playlist_page(id_playlist)

    return render_template('Playlist/add_playlist.html', user_image=upload_user_image())


@app.route('/addSongPlaylist/<id_song>/<id_playlist>/<id_playlist_arr>', methods=['GET', 'POST'])
@login_required
def add_song_playlist(id_song, id_playlist, id_playlist_arr):
    playlist_song = PlaylistSongs(id_song, id_playlist)
    db.session.add(playlist_song)
    db.session.commit()
    return redirect(url_for('playlist_page', id_playlist=id_playlist_arr))

