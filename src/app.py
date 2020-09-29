from src.db import get_db
from markupsafe import escape
from time import time
from flask import Blueprint, g, jsonify, request, abort
import logging
from src.db import query_db

logger = logging.getLogger(__name__)
router = Blueprint('routes', __name__)


@router.route('/')
def info():
    return 'Simple rating and download counter backend, see <a href="https://gitlab.com/banana-hackers/simple-ratings-server">gitlab.com/banana-hackers/simple-ratings-server</a>'


@router.route('/download_counter/', methods=['GET'])
@router.route('/download_counter', methods=['GET'])
def get_download_counts():
    # get download counts for all apps
    result = dict()
    for app in query_db('SELECT appid, count(*) as count FROM downloads GROUP BY appid'):
        result[app['appid']] = app['count']
    return jsonify(result)


@router.route('/download_counter/count/<appid_slug>')
def increase_download_counts(appid_slug):
    # count a download of the app with appid_slug
    cur = get_db().execute('INSERT INTO downloads (appid, timestamp) VALUES (?, ?)',
                           (escape(appid_slug).lower(), int(time())))
    get_db().commit()
    cur.close()
    return 'OK'


@router.route('/createuser', methods=['POST'])
def create_user():
    """
    create a user, that is able do create ratings
    """
    if not request.json \
            or not 'username' in request.json \
            or not 'logintoken' in request.json:
        abort(400)
    username = request.json['username']
    logintoken = request.json['logintoken']
    # CHECK: is nickname already taken?
    existing_users = query_db(
        'SELECT name FROM users WHERE name LIKE ? COLLATE NOCASE', (username, ))
    if len(existing_users) != 0:
        return dict(success=False, error="username is already taken"), 409
    # nickname is not taken, lets create the user
    cur = get_db().execute('INSERT INTO users (name,token,creationtime) VALUES (?, ?, ?)',
                           (username, logintoken, int(time())))
    get_db().commit()
    cur.close()
    return dict(success=True)


@router.route('/ratings/<appid_slug>', methods=['GET'])
def get_ratings(appid_slug):
    # get all ratings for an app
    appid = escape(appid_slug).lower()
    ratings = query_db(
        'SELECT r.points, r.description, r.creationtime, u.name AS username ' +
        'FROM ratings r, users u ' +
        'WHERE r.appid LIKE ? AND u.id=r.userid ' +
        'ORDER BY r.id DESC', (appid,))
    average = query_db(
        "SELECT AVG(points) as rating FROM ratings WHERE appid LIKE ?", (appid,))
    return dict(appid=appid, average=average[0]['rating'], ratings=ratings)


@router.route('/ratings/<appid_slug>/add', methods=['POST'])
def add_rating(appid_slug):
    # add a rating to an app
    appid = escape(appid_slug).lower()

    if not request.json \
            or not 'username' in request.json \
            or not 'logintoken' in request.json \
            or not 'points' in request.json \
            or not 'description' in request.json:
        abort(400)

    username = request.json['username']
    logintoken = request.json['logintoken']
    points = request.json['points']
    description = request.json['description']

    try:
        points = int(points)
        # CHECK has login token - to get the user
        found_users = query_db(
            'SELECT * FROM users WHERE name LIKE ? AND token == ?', (username, logintoken))
        if len(found_users) != 1:
            return dict(success=False, error="user not found"), 401
        user_id = found_users[0]['id']
        # CHECK is there already a rating by that person?
        found_ratings = query_db(
            'SELECT * FROM ratings WHERE appid LIKE ? AND userid == ?', (appid, user_id))
        if len(found_ratings) != 0:
            return dict(success=False, error="you already posted a review for this app"), 409
        # CHECK is rating valid
        if not (points >= 1 and points <= 5):
            return dict(success=False, error="rating can only be between 1 and 5"), 400
        # CHECK is the description filled out?
        if len(description) < 3:
            return dict(success=False, error="review description is to short"), 400

        cur = get_db().execute('INSERT INTO ratings (userid,appid,points,description,creationtime) VALUES (?, ?, ?, ?, ?)',
                               (user_id, appid, points, description, int(time())))
        get_db().commit()
        cur.close()
        return dict(success=True), 201
    except ValueError:
        return dict(success=False, error="value error, is your rating a number?"), 400
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e


@router.errorhandler(400)
def invalid_input(error):
    return dict(success=False, error="400 Bad Request"), 400


@router.errorhandler(500)
def invalid_input(error):
    return dict(success=False, error="500 An error occured"), 500
