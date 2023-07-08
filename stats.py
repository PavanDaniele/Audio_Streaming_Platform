import json

import auth
from app import *
from struttura_db import *

from artist import *

import datetime

def exits_song_playlist(id_song, id_playlist):

    song = db.session.query(PlaylistSongs).filter(PlaylistSongs.id_playlist == id_playlist)

    for s in song:
        if s.id_songs == id_song:
            return True

    return False


def insert_song_playlist(id_song, playlist):
    list_song_play = []
    for play in playlist:
        if not exits_song_playlist(id_song, play.id_playlist):
            list_song_play.append(play)

    return list_song_play

# function that upload the user image from Image in static path
def upload_user_image():
    return "Image/" + current_user.image


# ---------------------------------------------------Stats page---------------------------------------------------------


# check if the current user is an artist
def is_artist():
    art = db.session.query(Artists).filter(Artists.id_artists == current_user.id_users).first()
    if art:
        return True
    return False


# take a song using the id
def take_song(id_songs):
    song = db.session.query(Songs).filter(Songs.id_songs == id_songs).first()
    return song


# takes an artist using a song id
def take_artist(id_songs):
    song = take_song(id_songs)
    art = db.session.query(Artists).filter(Artists.id_artists == song.id_artist).first()
    return art


# ---------------------------------------------------Songs Stats--------------------------------------------------------


# function that passes the necessary data to make the statistics
@app.route('/songs_stats', methods=['GET', 'POST'])
@login_required
def songs_stats():
    title = ("Title", "length", "Date", "Type", "Listened")

    sl = db.session.query(SongsListened).order_by(SongsListened.id_users)
    number = []
    songs_name = []
    list_tmp = []
    count = 1
    for s in sl:
        if s.id_users == current_user.id_users:
            song_tmp = []
            prova = take_song(s.id_songs)
            song_tmp.append(count)
            song_tmp.append(prova.title)
            song_tmp.append(prova.length)
            song_tmp.append(prova.date_pub)
            song_tmp.append(prova.type)

            list_tmp.append(song_tmp)

            song = take_song(s.id_songs)
            if count <= 10:
                songs_name.append(song.title)
                number.append(s.num_times)
            count += 1

    song_list = tuple(list_tmp)

    return render_template('Stats/DashStats/songs_stats.html', headings=title, data=song_list, number=number,
                           songs_name=json.dumps(songs_name), artist_b=is_artist(), user_image=upload_user_image())


# ---------------------------------------------------Artists Stats------------------------------------------------------


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


# function that passes the necessary data to make the statistics
@app.route('/artists_stats', methods=['GET', 'POST'])
@login_required
def artists_stats():
    title = ("#", "Name", "Label", "Last Time")

    artis_listened = db.session.query(SongsListened).filter(SongsListened.id_users == current_user.id_users)
    artist_id = []
    count_times = []
    artists_name = []
    list_tmp = []
    count = 1
    for artists in artis_listened:

        listened = []
        prova = take_artist(artists.id_songs)

        if exists(artist_id, prova.id_artists):

            artist_id.append(prova.id_artists)
            listened.append(count)
            listened.append(prova.art_name)
            listened.append(prova.label)
            listened.append(artists.date_list)

            list_tmp.append(listened)
            if count <= 10:
                count_times.append(count_num(artis_listened, prova.id_artists))
                artists_name.append(prova.art_name)
            count += 1

    artists_list = tuple(list_tmp)

    return render_template('Stats/DashStats/artists_stats.html', headings=title, data=artists_list,
                           number=count_times, songs_name=json.dumps(artists_name), artist_b=is_artist(),
                           user_image=upload_user_image())


# ---------------------------------------------------Playlists Stats----------------------------------------------------

# check if a playlist is in the list
def exist_playlist(playlist_list_id, playlist_id):
    for playlist in playlist_list_id:
        if playlist == playlist_id:
            return False
    return True


# take an element from the Playlist tabel using the id
def take_playlist(playlist_id):
    prova = db.session.query(Playlist).filter(Playlist.id_playlist == playlist_id).first()
    return prova


def take_playlist_song(id_playlist):

    playlist_list = db.session.query(PlaylistSongs).filter(PlaylistSongs.id_playlist == id_playlist)
    return playlist_list


# count how many song is in the playlist
def count_playlist_song(playlist_id):
    pl = db.session.query(PlaylistSongs).filter(PlaylistSongs.id_playlist == playlist_id)
    count = 0
    for p in pl:
        count = count + 1
    return count


# function that passes the necessary data to make the statistics
@app.route('/playlists_stats', methods=['GET', 'POST'])
@login_required
def playlists_stats():
    headings = ["#", "Name", "Date Creation", "Description"]
    playlist_listened = db.session.query(PlaylistUsers).filter(PlaylistUsers.id_users == current_user.id_users)
    playlist_list = ()
    playlist_id = []
    take = []
    list_tmp = []
    count = 1
    for playlist in playlist_listened:
        listened = []
        prova = take_playlist(playlist.id_playlist)
        if exist_playlist(listened, playlist.id_playlist):
            listened.append(count)
            listened.append(prova.name)
            listened.append(prova.date_creation)
            listened.append(prova.description)

            list_tmp.append(listened)

            if count <= 10:
                playlist_id.append(prova.name)
                take.append(count_playlist_song(playlist.id_playlist))
            count += 1

    playlist_list = tuple(list_tmp)

    return render_template('Stats/DashStats/playlists_stats.html', headings=headings, data=playlist_list,
                           number=take, songs_name=json.dumps(playlist_id), artist_b=is_artist(),
                           user_image=upload_user_image())


# ---------------------------------------------------Type Stats--------------------------------------------------------


# function that passes the necessary data to make the statistics
@app.route('/types_stats', methods=['GET', 'POST'])
@login_required
def types_stats():
    title = ["#", "Name", "Last Time"]
    types_listened = db.session.query(SongsListened).filter(SongsListened.id_users == current_user.id_users)
    type_name = []
    count = []
    list_tmp = []
    count_s = 1
    for tl in types_listened:
        listened = []
        prova = take_song(tl.id_songs)
        if exists(type_name, prova.type):

            listened.append(count_s)
            listened.append(prova.type)
            listened.append(tl.date_list)
            list_tmp.append(listened)

            if count_s <= 10:
                type_name.append(prova.type)
                count.append(count_num(types_listened, prova.type))
            count_s = count_s + 1

    types_list = tuple(list_tmp)

    return render_template('Stats/DashStats/types_stats.html', headings=title, data=types_list,
                           number=count, songs_name=json.dumps(type_name), artist_b=is_artist(),
                           user_image=upload_user_image())

# ----------------------------------------------------Canzoni Consigliate-----------------------------------------------


# gives back a list of songs listened
def song_listened():
    types_listened = db.session.query(SongsListened).filter(SongsListened.id_users == current_user.id_users)
    list_tmp = []
    type_name = []
    for tl in types_listened:
        listened = []
        prova = take_song(tl.id_songs)
        if exists(type_name, prova.type):
            listened.append(prova.type)
            listened.append(count_num(types_listened, prova.type))
            list_tmp.append(listened)

    list_tmp.sort(key=lambda x: x[1], reverse=True)
    return list_tmp


# gives back a list of artist listened
def artist_listened():
    artis_listened = db.session.query(SongsListened).filter(SongsListened.id_users == current_user.id_users)
    artist_id = []
    list_tmp = []

    for artists in artis_listened:
        listened = []
        prova = take_artist(artists.id_songs)
        if exists(artist_id, prova.id_artists):
            listened.append(prova.id_artists)
            listened.append(count_num(artis_listened, prova.id_artists))
            list_tmp.append(listened)
            artist_id.append(prova.id_artists)

    list_tmp.sort(key=lambda x: x[1], reverse=True)
    return list_tmp


# check if an element is in the list
def is_accepted(song_list, elem):
    count = 0
    for s in song_list:
        count = count + 1
        if s[0] == elem and count <= 4:
            return True

    return False


# give a list of recommended songs
def song_cons():

    song_list = db.session.query(Songs)

    art = artist_listened()
    song = song_listened()
    list_end = []
    all_playlist = db.session.query(Playlist)

    count_song = 0

    for s in song_list:
        if is_accepted(song, s.type) or is_accepted(art, s.id_artist):
            tmp = []
            count_song += 1
            song_artist = db.session.query(Artists).filter(Artists.id_artists == s.id_artist).first()
            tmp.append(s)
            tmp.append(s.image)
            tmp.append(song_artist)
            tmp.append(str(datetime.timedelta(seconds=s.length)))
            tmp.append(count_song)
            tmp.append(insert_song_playlist(s.id_songs, all_playlist))
            list_end.append(tmp)

    return list_end







