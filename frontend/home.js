$(document).ready(function () {


    function changeUsername(username) {
        $("#username").text(username);
    }


    var socketio = io('/apsaperudo');

    // server to client events Handlers

    socketio.on('server_message', function (msg, cb) {

        console.log(msg);

        if (msg.message_type == 'connection_ok') {
            changeUsername(msg.player_id);
        }

        if (msg.message_type == 'player_id_changed') {
            changeUsername(msg.player_id);
        }

        if (msg.message_type == 'games_updated') {
            if (msg.games.length > 0) {
                var gameList = '<ul>';
                for (i = 0; i < msg.games.length; i++) {
                    gameList += `<li><a id="${msg.games[i]}" class="join_room" href="#">${msg.games[i]}</li>`
                }
                gameList += '</ul>';
                $("#games_list").html(gameList);
            } else {
                $("#games_list").html("No other games");
            }
        }

        if (msg.message_type == 'game_joined') {
            $("#player_game_name").text(msg.game_name);
        }

        $('#logs').append(`<br>[${msg.message_type}] : ${msg.message}`);

    });

    // client to server events

    $('form#change_username').submit(function (event) {
        socketio.emit('change_player_id', {
            new_player_id: $('#new_username').val()
        });
        return false;
    });

    $('form#new_game').submit(function (event) {
        socketio.emit('create_game', {
            game_id: $('#new_game_name').val()
        });
        return false;
    });

    $('#games').on('click', '.join_room', function (event) {
        socketio.emit('join_game', {
            game_id: $(event.target).attr('id')
        });
    });


});