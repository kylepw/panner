======
Panner
======
Django+Postgres+Redis-powered web app to keep track of friends.

Try it: https://panner.herokuapp.com

.. image:: screenshots/Panner.gif

Features
--------
- Supports: Meetup, Reddit, Spotify, and Twitter accounts.
- Simple, easy-to-navigate interface.
- Timesaver.
- Redis caching for faster load times.
- Mobile responsive.
- Robust test coverage.

Requirements
------------
- Python 3.6+
- API client ID/secret values
- Docker_ (highly recommended)

Client ID/Secret Values
-----------------------
.. _values:

- Before running this app, you must acquire client ID/secret values from services that you will use (one or more): Meetup_, Reddit_, Spotify_, and/or Twitter_. Use ``http://127.0.0.1:8000`` as the callback URI.

Run (in Docker)
-----------------
- Get Docker_.

- Clone, set values_, and run in **Django+Postgres+Redis+Gunicorn+Nginx** configuration: ::

    $ git clone https://github.com/kylepw/panner.git && cd panner
    $ cp env_template .env && vim .env
    $ docker-compose up --build

- Open ``http://127.0.0.1:8000`` in a browser.

Run (on Django development web server)
----------------------------------------
- Start Postgres and Redis servers (with Docker like here or another method): ::

    $ docker run --name db -p 5432:5432 -d postgres:11
    $ docker run --name redis -p 6379:6379 -d redis:5

- Clone, install dependencies, set values_, setup database, and run::

    $ git clone https://github.com/kylepw/panner.git && cd panner
    $ pip install pipenv && pipenv install
    $ cp env_template .env && vim .env
    $ pipenv shell
    (panner)$ # Postgres & Redis servers should be running at this point.
    (panner)$ export DB_HOST=127.0.0.1 REDIS_URL=redis://127.0.0.1:6379/1
    (panner)$ ./manage.py migrate && ./manage.py loaddata people
    (panner)$ DEBUG=1 ./manage.py runserver
    ...
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

- Open ``http://127.0.0.1:8000`` in a browser.

Tests
-----
- Run Django tests from top of project::

    $ pipenv shell
    (panner)$ docker run --name db -p 5432:5432 -d postgres:11
    (panner)$ docker run --name redis -p 6379:6379 -d redis:5
    (panner)$ export DB_HOST=127.0.0.1 REDIS_URL=redis://127.0.0.1:6379/1
    (panner)$ python manage.py test

- Run api unit tests from sns directory::

    $ pipenv shell && cd sns
    sns (panner)$ python -m unittest discover api

Todo
----
- Add Github API support.
- Multiple user account support.

License
-------
`MIT License <https://github.com/kylepw/panner/blob/master/LICENSE>`_

.. _Docker: https://www.docker.com/products/docker-desktop
.. _Meetup: https://www.meetup.com/meetup_api/
.. _Reddit: https://www.reddit.com/prefs/apps
.. _Spotify: https://developer.spotify.com/dashboard/login
.. _Twitter: https://developer.twitter.com/en/apply/user
