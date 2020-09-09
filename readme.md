# Simple appstore rating server

instructions are for linux and mac, you'll need to change some commands to make it work on windows.
## Instalation

```bash
virtualenv .venv
source .venv/bin/activate
pip install Flask flask-cors
```

## Usage

```bash
source .venv/bin/activate
export FLASK_APP=src/app.py
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

### Deployment with UWSGI

```sh
source .venv/bin/activate
pip install uwsgi
# test with
uwsgi uwsgi.ini
```
next setup a daemon, like described in https://lab.uberspace.de/guide_flask.html#setup-daemon

## Technology

https://flask.palletsprojects.com/en/1.1.x/
https://docs.python.org/3/library/sqlite3.html
https://sqlitebrowser.org/

## Plan
rough plan

### Anonymous download count

#### POST increase download count

-> store in db: appid, time of download

#### GET downloads

-> json {[key:appid]:downloads}


### Rating server

#### POST create Account

- (does nickname is already taken?)

-> store in db: userid, nickname, date of account creation, login token

#### POST create rating

- (has login token - to get the user)
- (is there already a rating by that person?)
- (is the description filled out?)

-> store in db:  userid, appid, rating, description, date

#### GET ratings for appid

-> {
 overall_rating,
 ratings:{name, rating, description, date}[]
}



### Improvement ideas:

- spam protection
- ability to update a rating
- moderation user interface
- cache download counts somehow?