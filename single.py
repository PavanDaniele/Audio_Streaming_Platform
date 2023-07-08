import json

from app import *
from auth import *
from stats import *
from stats import take_song, take_playlist
from struttura_db import *


def get_album():
    album_list = db.session.query(Album).filter(Album.id_artist == current_user.id_users)
    album = []
    for al in album_list:
        tmp = []
        tmp.append(al)
        tmp.append(db.session.query(Artists).filter(Artists.id_artists == al.id_artist).first())
        album.append(tmp)

    return album


@app.route('/album_list_page', methods=['GET', 'POST'])
@login_required
def album_list_page():

    album_list = get_album()

    return render_template('Album/album_list.html', album=album_list, user_image=upload_user_image())


def exists_song_album(id_song, id_album):
    song_album = db.session.query(SongsAlbum).filter(SongsAlbum.id_album == id_album)

    for sa in song_album:
        if sa.id_songs == id_song:
            return True

    return False


def take_song_album(id_album):
    song_album = db.session.query(SongsAlbum).filter(SongsAlbum.id_album == id_album)
    songs = []

    for al in song_album:
        if not exists_song_album(al.id_songs, id_album):
            songs.append(al)

    return songs


@app.route('/album_page/<id_album>', methods=['GET', 'POST'])
@login_required
def album_page(id_album):

    title = ("#", "Title", "Artist", "length", "Date", "Type")

    album = db.session.query(SongsAlbum).filter(SongsAlbum.id_album == id_album)
    list_tmp = []
    count = 0
    for al in album:
        song_tmp = []
        count = count + 1
        prova = take_song(al.id_songs)
        song_tmp.append(count)
        song_tmp.append(prova.title)
        art = db.session.query(Artists).filter(Artists.id_artists == prova.id_artist).first()
        song_tmp.append(art.art_name)
        song_tmp.append(prova.length)
        song_tmp.append(prova.date_pub)
        song_tmp.append(prova.type)
        list_tmp.append(song_tmp)

    song_list = tuple(list_tmp)
    album_list = get_album()
    play = db.session.query(Album).filter(Album.id_album == id_album).first()
    song_choose = take_song_album(id_album)
    artist = db.session.query(Artists).filter(Artists.id_artists == play.id_artist).first()

    return render_template('Album/album.html', headings=title, data=song_list, albums=album_list,
                           album_obj=play, artist_obj=artist, song_choose=song_choose, user_image=upload_user_image())

# ----------------------------------------------------Add Album-Song-----------------------------------------------


@app.route('/add')
@login_required
def add():

    check = current_user.is_artist()#Un check in più non fa mai male...
    if check:
        return render_template('/Home/add.html', user_image=upload_user_image())
    else:
        render_template('/Home/home.html', user_image=upload_user_image())


@app.route('/add_album', methods=['GET', 'POST'])
@login_required
def add_single():
    if request.method == 'POST':
        #Mi faccio fare il form in forma di dizionario
        form = request.form
        #Mi salvo il nome dell'album
        album_name = form.get('album_name')

        #Mi faccio delle liste con ogni parametro: titolo, lunghezza, genere
        titles = form.getlist('title')
        lengths = form.getlist('length')
        genres = form.getlist('type')
        #Conto quante canzoni devo inserire
        counter = titles.__len__()
        image_album = 'images.jpeg'
        #Creo oggetto album
        album = Album(current_user.id_users, date.today(), album_name, image_album)

        #Aggiungo l'album al db
        db.session.add(album)
        db.session.commit()
        #Qua dentro mi salvo gli id delle canzoni che ho appena inserito
        song_ids = []

        #Inserisco con un ciclo for le canzoni
        for i in range(0, counter):
            song = Songs(current_user.id_users, titles[i], lengths[i], date.today(), genres[i], image_album)
            # Aggiungo la canzone
            db.session.add(song)
            db.session.commit()
            # Mi salvo il
            song_ids.append(last_song_id())

        # Associo le canzoni inserite all'album inserito
        x = song_ids.__len__()

        for j in range(0, x):
            print('Provo a inserire:')
            print(last_album_id(), song_ids[j])

            song_album = SongsAlbum(last_album_id(), song_ids[j])

            db.session.add(song_album)
            db.session.commit()

        return redirect(url_for('home'))

    return render_template('Album/add_album.html', user_image=upload_user_image())


def last_song_id():
    # So che l'id è sequenziale, quindi ritorno il valore massimo
    return db.session.query(func.max(Songs.id_songs)).first()[0]


def last_album_id():
    # So che l'id è sequenziale, quindi ritorno il valore massimo
    return db.session.query(func.max(Album.id_album)).first()[0]

@app.route('/add_single')
@login_required
def add_single():

    return render_template('Home/add_single.html', user_image=upload_user_image())
