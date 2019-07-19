======
Panner
======
Django-powered web app to keep track of friends' social network activity.

Try it **now** with Docker_:

*Coming soon*

.. _Docker: https://docs.docker.com/docker-for-mac/install/

.. image:: screenshots/activity.png

Features
--------
- Supports: Meetup, Reddit, Spotify, and Twitter accounts.
- Simple, easy-to-navigate interface.
- Timesaver.
- Robust test coverage.

Requirements
------------
- Python 3.6+
- PostgreSQL
- pipenv (recommended)

Setup
-----
- Acquire API client ID and secrets from Meetup_, Reddit_, Spotify_, and Twitter_ (use http://127.0.0.1:8000 as callback URI).

.. _Meetup: https://www.meetup.com/meetup_api/
.. _Reddit: https://www.reddit.com/prefs/apps
.. _Spotify: https://developer.spotify.com/dashboard/login
.. _Twitter: https://developer.twitter.com/en/apply/user

- Setup a PostgreSQL server locally with a database and username/password with...

    Docker_ (``DB_NAME`` and ``DB_USER`` values will be ``postgres``)::

    $ docker run --name panner-db -e POSTGRES_PASSWORD=mypasswd -d postgres

    -OR- MacOS_ or Linux_.

.. _Docker: https://docs.docker.com/docker-for-mac/install/
.. _MacOS: https://www.robinwieruch.de/postgres-sql-macos-setup/
.. _Linux: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

Run
---
- Clone it, install dependencies, configure environment variables, migrate DB, and run::

    $ git clone https://github.com/kylepw/panner.git && cd panner
    $ pip install pipenv && pipenv install
    $ cp env_template .env && vim .env #Insert your values.
    $ pipenv shell
    $ # Make sure you have PostgreSQL setup and running at this point.
    $ python manage.py migrate
    $ python manage.py runserver
    ...
    Django version 2.2.3, using settings 'panner.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

- Access http://127.0.0.1:8000 from your favorite browser.

Todo
----
- Docker image running with PostgreSQL and Nginx.
- More tests.
- Caching.
- Multiple user account support.

License
-------
`MIT License <https://github.com/kylepw/panner/blob/master/LICENSE>`_
