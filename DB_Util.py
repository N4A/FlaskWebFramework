import sqlite3
from flask import g

DATABASE = 'static/database.db'
SCHEMA = 'static/schema.sql'


def init_db(app, schema=SCHEMA):
    """
    init the database with the schema
    :param app: Flask app
    :param schema: schema file path
    :return:
    """
    with app.app_context():
        db = get_db()
        with app.open_resource(schema, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db(db_url=DATABASE):
    """
    get a unique db connection
    :return: a db connection object
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_url)
    db.row_factory = sqlite3.Row
    return db


def db_query(db, query_sql, args=(), one=False):
    """
    execute a query sql, the db is usually the default one _DATABASE
    :param query_sql:
    :param args:
    :param one: decide whether to return one record or not
    :param db: decide to query which db, the default one is _DATABASE
    :return:
    """
    cur = db.execute(query_sql, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv



