$(document).ready(function () {

    console.log('hello');

    var socketio = io('/apsaperudo');

    // server to client events Handlers

    socketio.on('server_message', function (msg, cb) {

        console.log(msg);

        if (msg.message_type == 'connection_ok') {
            $("#username").text(msg.username);
        }

        if (msg.message_type == 'games_updated') {
            var lists = "";
            for (i = 0; i < msg.games.length; i++) {
                lists += `<li><a id="${msg.games[i]}" class="join_room" href="#">${msg.games[i]}</li>`
            }
            $("#games_list").html(lists);
        }

        if (msg.message_type == 'game_joined') {
            $("#player_game_name").text(msg.game_id);
        }

        $('#logs').append(`<br>[${msg.message_type}] : ${msg.message}`);

    });

    // client to server events

    $('#games').on('click', '.join_room', function (event) {
        socketio.emit('join_game', {
            game_id: $(event.target).attr('id'),
            username: $('#username').text()
        });
    });


});