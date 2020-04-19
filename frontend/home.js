$(document).ready(function () {


    function changeUsername(username) {
        $("#username").text(username);
    }


    var socketio = io('/apsaperudo');

    // server to client events Handlers

    socketio.on('server_message', function (msg, cb) {

        console.log(msg);

        if (msg.message_type == 'connection_ok') {
            changeUsername(msg.username);
        }

        if (msg.message_type == 'username_changed') {
            changeUsername(msg.username);
        }

        if (msg.message_type == 'games_updated') {
            if (msg.games.length > 0) {
                var gameList = '<ul>';
                for (i = 0; i < msg.games.length; i++) {
                    lists += `<li><a id="${msg.games[i]}" class="join_room" href="#">${msg.games[i]}</li>`
                }
                gameList += '</ul>';
                $("#games_list").html(gameList);
            } else {
                $("#games_list").html("No other games");
            }
        }

        if (msg.message_type == 'game_joined') {
            $("#player_game_name").text(msg.game_id);
        }

        $('#logs').append(`<br>[${msg.message_type}] : ${msg.message}`);

    });

    // client to server events

    $('form#change_username').submit(function (event) {
        console.log("change_username");
        socketio.emit('change_username', {
            new_username: $('#new_username').val()
        });
        return false;
    });

    $('#games').on('click', '.join_room', function (event) {
        socketio.emit('join_game', {
            game_id: $(event.target).attr('id'),
            username: $('#username').text()
        });
    });


});