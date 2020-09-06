import sqlite3
from markupsafe import escape
from flask import Flask, g, jsonify
app = Flask(__name__)

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

        def make_dicts(cursor, row):
            return dict((cursor.description[idx][0], value)
                        for idx, value in enumerate(row))
        db.row_factory = make_dicts
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


init_db()


@app.route('/')
def info():
    return 'Todo, add information here'


@app.route('/download_counter', methods=['GET'])
def get_download_counts():
    # get download counts for all apps
    result = dict()
    for app in query_db('SELECT appid, count(*) as count FROM downloads GROUP BY appid'):
        result[app['appid']] = app['count']
    return jsonify(result)


@app.route('/download_counter/count/<appid_slug>')
def increase_download_counts(appid_slug):
    # count a download of the app with appid_slug
    cur = get_db().execute('INSERT INTO downloads (appid, timestamp) VALUES (?, ?)',
                           (escape(appid_slug), 342142))
    get_db().commit()
    cur.close()
    return 'OK'
