var i = 1;

function add_track(){
    i++;
    $('#tabella_canzoni').find('tbody').append('<tr><th scope="row" name="n_song" id="n_song"><input type="hidden" value="'+i+'">'+i+'</th>' +
        '                                           <td><input class="form-control rounded-0" type="text" name="title" id="title" placeholder="Title"></td>' +
        '                                           <td><input class="form-control rounded-0" type="text" name="length" id="length" placeholder="Length"></td>' +
        '                                           <td><input class="form-control rounded-0" type="text" name="type" id="type" placeholder="Genre"></td>' +
        '                                           <td></td>' +
        '                                       </tr>');
}