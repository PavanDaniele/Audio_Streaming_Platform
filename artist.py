import json

from app import *
from auth import *
from stats import *
from struttura_db import *
import datetime


# take a song using the id
def take_song(id_songs):
    song = db.session.query(Songs).filter(Songs.id_songs == id_songs).first()
    return song


# check if an element is in the list
def exists(list_id, elem_id):
    for ld in list_id:
        if ld == elem_id:
            return False
    return True


# count how many element is in the list
def count_num(list_id, elem_id,):
    count = 0
    for art in list_id:
        prova = take_song(art.id_songs)
        if prova.id_artist == elem_id or prova.type == elem_id:
            count = count + art.num_times
    return count


def upload_user_image():
    return "Image/" + current_user.image


def is_artist():
    art = db.session.query(Artists).filter(Artists.id_artists == current_user.id_users)
    count = 0
    for a in art:
        count = count +1

    if count >= 1:
        return True
    return False


def count_song(id_song):

    song = db.session.query(SongsListened).filter(SongsListened.id_songs == id_song)
    x = 0
    for s in song:
        x = x + s.num_times
    return x


def id_play():
    playlist = db.session.query(Playlist).order_by(Playlist.id_playlist.desc()).first()
    return playlist.id_playlist


def get_artist(id):
    artist = db.session.query(Artists).filter(Artists.id_artists == id).first()

    return artist


def get_artist_albums(id):
    albums = db.session.query(Album).filter(Album.id_artist == id).all()

    return albums


def get_artist_songs(id):
    songs = db.session.query(Songs).filter(Songs.id_songs == id).all()

    return songs


@app.route('/song_ar', methods=['GET', 'POST'])
@login_required
def song_ar():

    title = ("Title", "length", "Date", "Type", "Listened")
    sl = db.session.query(Songs).filter(Songs.id_artist == current_user.id_users)
    number = []
    songs_name = []
    list_tmp = []
    count = 0
    for s in sl:
        song_tmp = []
        x = count_song(s.id_songs)
        song_tmp.append(s.title)
        song_tmp.append(s.length)
        song_tmp.append(s.date_pub)
        song_tmp.append(s.type)
        song_tmp.append(x)
        list_tmp.append(song_tmp)
        if count <= 10:
            songs_name.append(s.title)
            number.append(x)
        count = count + 1

    list_tmp.sort(key=lambda x:x[4], reverse=True)
    song_list = tuple(list_tmp)

    return render_template('Stats/Artist/songs_artist.html', headings=title, data=song_list, number=number,
                           songs_name=json.dumps(songs_name), artist_b=is_artist(), user_image=upload_user_image())


@app.route('/types_stats_artist', methods=['GET', 'POST'])
def types_stats_artist():
    title = ["Name", "Number of Times"]
    list_type = db.session.query(Songs).filter(Songs.id_artist == current_user.id_users)
    song_type_listened= db.session.query(SongsListened)
    end_list = []
    prova = []
    number = []
    songs_name = []
    count = 1
    for t in list_type:
        if exists(prova, t.type):
            tmp = []
            prova.append(t.type)
            tmp.append(t.type)
            tmp.append(count_num(song_type_listened, t.type))
            end_list.append(tmp)
            if count <= 10:
                number.append(count_num(song_type_listened, t.type))
                songs_name.append(t.type)
            count += 1

    end_list.sort(key=lambda x: x[1], reverse=True)
    return render_template('Stats/Artist/types_artist.html', headings=title, data=end_list, number=number,
                           songs_name=json.dumps(songs_name), artist_b=is_artist(), user_image=upload_user_image())


def count_album(id_album):
    al = db.session.query(SongsAlbum).filter(SongsAlbum.id_album == id_album)
    x = 0
    for a in al:
        x = x + count_song(a.id_songs)

    return x


@app.route('/album_ar', methods=['GET', 'POST'])
@login_required
def alb_ar():
    title = ("Title", "Date", "Listened")

    sl = db.session.query(Album).filter(Album.id_artist == current_user.id_users)
    number = []
    songs_name = []
    list_tmp = []
    count = 0
    for s in sl:
        song_tmp = []
        x = count_album(s.id_album)
        song_tmp.append(s.title)
        song_tmp.append(s.date_pub)
        song_tmp.append(x)
        list_tmp.append(song_tmp)
        if count <= 10:
            songs_name.append(s.title)
            number.append(x)
        count = count + 1

    list_tmp.sort(key=lambda x: x[2], reverse=True)
    song_list = tuple(list_tmp)
    return render_template('Stats/Artist/albums_artist.html', headings=title, data=song_list, number=number,
                           songs_name=json.dumps(songs_name), artist_b=is_artist(), user_image=upload_user_image())


def artist_song_page(artist):
    song = db.session.query(Songs).filter(Songs.id_artist == artist.id_artists)
    song_list = []


    for s in song:
        tmp = []
        tmp.append(s)
        tmp.append("Image/"+s.image)
        tmp.append(artist)
        tmp.append(str(datetime.timedelta(seconds=s.length)))

        song_list.append(tmp)

    return song_list


def artist_album_page(artist):
    album = db.session.query(Album).filter(Album.id_artist == artist.id_artists)
    album_list = []

    for al in album:
        tmp = []
        tmp.append(al)
        tmp.append("Image/"+al.image)
        tmp.append(artist)
        tmp.append(al.date_pub)
        album_list.append(tmp)

    return album_list


@app.route('/artist_profile_page/<int:id_artists>', methods=['GET', 'POST'])
@login_required
def artist_profile_page(id_artists):

    artist = get_artist(id_artists)
    song = artist_song_page(artist)
    album = artist_album_page(artist)

    user_artist = db.session.query(Users).filter(Users.id_users == id_artists).first()
    artist_image = "Image/" + user_artist.image

    return render_template('Profile/artist.html', artist=artist, album=album, user_image=upload_user_image(),
                           artist_image=artist_image, user_artist=user_artist, song=song)



