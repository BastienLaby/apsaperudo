# apsaperudo backend

Apsaperudo backend made with Flask.

### Requirements
- python 3.7
- sqlite
- Flask (flask-sqlalchemy, flask-migrate, flask-socketio)


### Backend installation

- Open a terminal
- Move into backend directory : `cd backend/`
- Create a virtualenv : `py -3.7 -m venv .`
- Activate the env : `./Scripts/activate.bat` (Windows) `source venv/bin/active` (Linux)
- Install dependencies : `pip install -r requirements.txt`

### Backend startup

Simply : `python apsaperudo/application.py`

Avoid `flask run` because of **flask-Socketio** (see [documentation](https://flask-socketio.readthedocs.io/en/latest/#initialization)).

### Setup database

`flask db init`
`flask db migrate`
`flask db upgrade`

# backend structure

## Modules and layers

The backend consists of three layers :
- the *database* layer, wich manipulate the database.
- the *application* layer, which contains the game & lobby logic.
- the *client* layer, which interacts with the client.

The *database* layer uses the **apsaperudo.api** submodule. The *application* layer uses the **apsaperudo.engine** submodule, and the *clien*t layer uses **Flask routing** and **socketio connections**.

Each layer represents the same concepts (game, players, ...) using different data structure. Each layer is independent from the others layers and communicates with them using the **io** module.

## The "io" module

The **io** module (**i**nput/**o**utput) provide functions to serialize data structures between backend layers :
- serialize *database* data to *application* data
- serialize *application* data to *database* data
- serialize *application* data to *client* data
- serialize *client* data to *application* data


### Data structures

#### Database structures

#### Engine structures

#### Client structures

