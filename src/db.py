import sqlite3
from flask import g, current_app


def get_db():
    """
    get a connection to the database that is reused during one request and closed again after the request ends
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config['DATABASE'])

        def make_dicts(cursor, row):
            return dict((cursor.description[idx][0], value)
                        for idx, value in enumerate(row))
        db.row_factory = make_dicts
    return db


def init_db(app):
    """
    Initializes the db: creates tables if they don't exist
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
