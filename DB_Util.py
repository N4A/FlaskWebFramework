import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.user import User

DATABASE = 'static/database.db'
sqlalchemy_db = 'sqlite:///' + DATABASE
SCHEMA = 'static/schema.sql'


def init_db(schema=SCHEMA):
    """
    init the database with the schema
    :param schema: schema file path
    :return:
    """
    db = get_db()
    c = db.cursor()
    with open(schema, mode='r') as f:
        c.executescript(f.read())
    db.commit()
    db.close()


def get_db(db_url=DATABASE):
    """
    get a unique db connection
    :return: a db connection object
    """
    db = sqlite3.connect(db_url)
    db.row_factory = sqlite3.Row
    return db


def get_sesion(url=sqlalchemy_db):
    # 初始化数据库连接:
    engine = create_engine(url)
    # 创建DBSession类型:
    return sessionmaker(bind=engine)()


# test db
if __name__ == '__main__':
    # init_db,!!!!! delete the old one and create the new one
    init_db()
    print('create db: ok')
    # test sqlalchemy
    sess = get_sesion()
    sess.add(User(id=1, name='Test', passwd='Test'))
    sess.commit()
    print('test insert user(name=Test, passwd=Test): ok')

    user = sess.query(User).one()
    print('test reading user from the database: ')
    print('user: ', user)
    print('print message of the user: ')
    print('name: ', user.name, ', passwd', user.passwd)
    sess.close()
    print('The database works well.')
