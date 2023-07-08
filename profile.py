import json

from app import *
from auth import *
from stats import *
from stats import take_song, take_playlist
from struttura_db import *

list_image = ['chicken-avatar.png', 'monster-avatar.png', 'panda-avatar.png', 'penguin-avatar.png', 'yellow-avatar.jpeg',
              'Netflix-avatar.png']
ARTIST_BOOL = False
# ----------------------------------------------------Artist------------------------------------------------------------


def prova_art():
    if is_artist():
        return True
    else:
        return False


def stats_types():
    list_type = db.session.query(Songs).filter(Songs.id_artist == current_user.id_users)
    list_listened = db.session.query(SongsListened)
    end_list = []
    prova = []
    for t in list_type:
        if exists(prova, t.type):
            tmp = []
            prova.append(t.type)
            tmp.append(t.type)
            tmp.append(count_num(list_listened, t.type))
            end_list.append(tmp)

    return end_list


def stats_album():
    list_album = db.session.query(Album).filter(Album.id_artist == current_user.id_users)
    album = []
    count = 1
    for al in list_album:
        if count < 5:
            tmp = []
            tmp.append(al)
            tmp.append(count_album(al.id_album))
            album.append(tmp)
            count += 1
        else:
            return album

    return album


def count_song_listened(id_song):
    song = db.session.query(SongsListened).filter(SongsListened.id_songs == id_song)
    count = 0
    for s in song:
        count += s.num_times

    return count


def stats_song():
    song = db.session.query(Songs).filter(Songs.id_artist == current_user.id_users)
    song_list = []
    count = 0
    for s in song:
        count += 1
        if count <= 5:
            tmp = []
            tmp.append(s)
            tmp.append(count_song_listened(s.id_songs))
            song_list.append(tmp)

    return song_list


def upload_user_image():
    return "Image/" + current_user.image


@app.route('/artist_page',  methods=['GET', 'POST'])
def artist_page():

    artist_user = db.session.query(Artists).filter(Artists.id_artists == current_user.id_users).first()

    user_image = "Image/" + current_user.image

    song = stats_song()

    type_list = stats_types()
    album_list = stats_album()
    ARTIST_BOOL = True

    return render_template('Profile/profile_artist.html', IS_ARTIST= prova_art(), artist=artist_user,
                           user_image=upload_user_image(), type=type_list, album=album_list,
                           song=song, artist_bool=True)


# ----------------------------------------------------Listener----------------------------------------------------------

def listener_type(num):
    song_list = db.session.query(SongsListened).filter(SongsListened.id_users == current_user.id_users)
    type_list = []
    end_list = []

    count = 0
    for sl in song_list:
        song = take_song(sl.id_songs)
        count += 1
        if exists(type_list, song.type) and count <= num:
            tmp = []
            tmp.append(song.type)
            tmp.append(count_num(song_list, song.type))
            end_list.append(tmp)

    return end_list


def listener_song(num):
    song_list = db.session.query(SongsListened).filter(SongsListened.id_users == current_user.id_users)
    end_list = []
    count = 0
    for sl in song_list:
        count += 1
        if count <= num:
            tmp = []
            tmp.append(take_song(sl.id_songs))
            tmp.append(sl)
            end_list.append(tmp)

    return end_list


def listener_artist(num):

    artist_list = db.session.query(SongsListened).filter(SongsListened.id_users == current_user.id_users)
    artist_id = []
    list_tmp = []
    count = 0
    for artists in artist_list:
        prova = take_artist(artists.id_songs)
        count += 1
        if exists(artist_id, prova.id_artists) and count <= num:
            listened = []
            artist_id.append(prova.id_artists)
            listened.append(prova)
            listened.append(count_num(artist_list, prova.id_artists))
            list_tmp.append(listened)

    return list_tmp


def listener_playlist(num):
    playlist_listened = db.session.query(PlaylistUsers).filter(PlaylistUsers.id_users == current_user.id_users)
    list_tmp = []
    count = 1
    for playlist in playlist_listened:
        listened = []
        prova = take_playlist(playlist.id_playlist)
        count += 1
        if exist_playlist(listened, playlist.id_playlist) and count <= num:
            listened.append(prova)
            listened.append(take_playlist_song(playlist.id_playlist))

            list_tmp.append(listened)

    return list_tmp


@app.route('/listener_page', methods=['GET', 'POST'])
def listener_page():
    dim = 5
    user_image = "Image/" + current_user.image
    type_list = listener_type(dim)
    song_list = listener_song(dim)
    artist_list = listener_artist(dim)
    playlist_list = listener_playlist(dim)
    ARTIST_BOOL = False
    return render_template('Profile/profile_listener.html', IS_ARTIST=prova_art(), user_image=upload_user_image(),
                           type=type_list, song=song_list,artist=artist_list, playlist=playlist_list, artist_bool=False)

# ----------------------------------------------------Change Icon-------------------------------------------------------


@app.route('/change_avatar', methods=['GET', 'POST'])
def change_avatar():

    images = []

    for ls in list_image:
        tmp = []
        tmp.append(os.path.join(app.config['UPLOAD_FOLDER'], ls))
        tmp.append(ls)
        images.append(tmp)

    return render_template('Profile/avatar_change.html', images=images)


@app.route('/choose_avatar/<name_avatar>', methods=['GET', 'POST'])
def choose_avatar(name_avatar):

    if request.method == 'GET':
        print(name_avatar)
        current_user.image = name_avatar
        db.session.commit()

        if ARTIST_BOOL:
            return redirect(url_for('artist_page'))
        else:
            return redirect(url_for('listener_page'))

