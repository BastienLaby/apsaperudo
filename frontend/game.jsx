'use strict';

const e = React.createElement;

class Game extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: null,
            players: null
        };
    }

    return(
        <button onClick = {() => this.setState({ liked: true })}>
            Like
        </button >
    );
}

const domContainer = document.querySelector('#game_container');
ReactDOM.render(e(LikeButton), domContainer);