from playlist import insert_song_playlist
from struttura_db import *
import datetime


def under_number(count):
    if count % 4 == 0:
        elem_artist = int(count / 4)
    else:
        elem_artist = int((count / 4) + 1)
    return count


# Song
def song_list():
    songs = db.session.query(Songs)
    list_song_image = []
    count_song = 0
    all_playlist = db.session.query(Playlist)

    for song in songs:
        tmp = []
        count_song += 1
        song_artist = db.session.query(Artists).filter(Artists.id_artists == song.id_artist).first()
        tmp.append(song)
        tmp.append(song.image)
        tmp.append(song_artist)
        tmp.append(str(datetime.timedelta(seconds=song.length)))
        tmp.append(count_song)
        tmp.append(insert_song_playlist(song.id_songs, all_playlist))
        list_song_image.append(tmp)

    return list_song_image


# Playlist
def playlist_list():
    playlist = db.session.query(Playlist).filter(Playlist.private == False)
    count_play = 0
    list_playlist_image = []

    for play in playlist:
        count_play += 1
        tmp = []
        tmp.append(play)
        tmp.append(os.path.join(app.config['UPLOAD_FOLDER'], "playlist_def.jpeg"))
        tmp.append(count_play)
        list_playlist_image.append(tmp)

    return list_playlist_image


# Artist
def artist_list():
    artist = db.session.query(Artists)
    list_artist_image = []
    count_art = 0

    for art in artist:
        count_art += 1
        tmp = []
        tmp.append(art)
        elem = db.session.query(Users).filter(Users.id_users == art.id_artists).first()
        tmp.append(os.path.join(app.config['UPLOAD_FOLDER'], elem.image))
        tmp.append(count_art)
        list_artist_image.append(tmp)

    return list_artist_image


# Album
def album_list():
    album = db.session.query(Album)
    list_album_image = []
    count_album = 0

    for al in album:
        count_album += 1
        tmp = []
        tmp.append(al)
        tmp.append(os.path.join(app.config['UPLOAD_FOLDER'], al.image))
        tmp.append(count_album)
        list_album_image.append(tmp)

    return list_album_image


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    best_playlist = db.session.query(Playlist).filter(Playlist.name == 'Preferiti').first()
    user_image = "Image/" + current_user.image
    playlist_logo_love = os.path.join(app.config['UPLOAD_FOLDER'], "heart.jpeg")
    playlist_wallpaper = os.path.join(app.config['UPLOAD_FOLDER'], "playlist_wallpaper.jpg")
    all_playlist = db.session.query(Playlist)

    list_song_image = song_list()
    list_artist_image = artist_list()
    list_playlist_image = playlist_list()
    list_album_image = album_list()

    return render_template('Search/search.html', search_bar=True, user_image=user_image, artists=list_artist_image,
                           playlist=list_playlist_image, songs=list_song_image, album=list_album_image,
                           playlist_logo=playlist_logo_love, playlist_wallpaper=playlist_wallpaper,
                           best_playlist=best_playlist, all_playlist=all_playlist)
