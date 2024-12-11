# Character Sheet Web App

This web application allows users to create and manage character sheets for any RPG.

## Features

- Create new characters with default attributes and skills.
- Edit character details, attributes, skills, talents, armor, weapons, spells, and trappings.
- View character sheets in a structured format.

## ToDo

- Make table cells change to input on click and back again when saving to make everything more homogenous

## Serving The Application Locally

**Windows** (development):

Using _**UV**_:

```{cmd}
cd 'path/to/character_creator_project/'
```

Serving for the hosting machine only:

```{cmd}
$j1 = uv run flask --app src/main run --debug 2>&1 > output.log &
```

Serving for hosting machine and check on mobile or tablet:

```{cmd}
$j1 = uv run flask --app src/main run -h 0.0.0.0 --debug 2>&1 > output.log &
```

to keep it running in the terminal remove the last `&`

### Windows

Using _**UV**_ :

```{cmd}
cd 'path/to/character_creator_project/'
```

```{cmd}
$j1 = uv run waitress-serve --host 127.0.0.1 --port 5000 src:app 2>&1 > output.log &
```

## Database migration

To be sure that the database is up and running as it should be
please check that the database path corresponds to each other in `alembic.ini`, `src/main.py`, and the name of the database itself.

### alembic.ini

```{code}
# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = sqlite:///instance/CharSheet.db
```

### src/main.py

```{code}
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///CharSheet.db"  <----- this line right here
app.config["SECRET_KEY"] = "your_secret_key"  # Needed for flashing messages
db.init_app(app)
```

please note the path difference in the example above.
The alembic needs the instance directory as well, where src/main only needs the name of the database.

When both paths correspond to the database file name run the following command:

```{code}
uv run alembic upgrade head
```

The database is now up to date.

Have fun!
