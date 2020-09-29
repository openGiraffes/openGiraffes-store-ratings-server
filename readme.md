# Simple appstore rating server

instructions are for linux and mac, you'll need to change some commands to make it work on windows.

## Instalation

```bash
virtualenv .venv
source .venv/bin/activate
pip install Flask flask-cors pytest
```

## Usage

```bash
source .venv/bin/activate
export FLASK_APP=main.py
# start server localy
flask run
# to run it that it is availible on the network
# run this instead
flask run --host=0.0.0.0
```

### Deployment

for deployment see:
https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment
https://lab.uberspace.de/guide_flask.html
https://gunicorn.org/

#### Deployment with UWSGI

```sh
source .venv/bin/activate
pip install uwsgi
# test with
uwsgi uwsgi.ini
```

next setup a daemon, like described in https://lab.uberspace.de/guide_flask.html#setup-daemon

## Development

### Testing

```bash
source .venv/bin/activate
pytest
```

### Improvement ideas:

- spam protection
- ability to update a rating
- moderation user interface
- cache download counts somehow?
- pagination of ratings (if we have so many that we need it)

## Notes for implementing this app in an store app

### Documentation

The documentation can be found in [docs.md](./docs.md).

### XSS - Warning

The description and username are NOT sanitized from html so DO NOT render them directly as html.
This would make an XSS cross-site-scripting attack possible. (someone writing a script tag in an rating description that you excecute because you rendered it as html. this script can contain malware and viruses).

> **NEVER TRUST USER INPUT!**

for futher information on xss attacks see:

- https://www.youtube.com/watch?v=EoaDgUgS6QA - an explaination video about xss
- https://old.liveoverflow.com/web_security/xss.html
- https://en.wikipedia.org/wiki/Cross-site_scripting


## Technology

https://flask.palletsprojects.com/en/1.1.x/
https://docs.python.org/3/library/sqlite3.html
https://sqlitebrowser.org/