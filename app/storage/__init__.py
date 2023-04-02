"""
storage包括 sql db / nosql db / 文件存储 等
"""
import os
import sqlite3
from typing import Optional

from flask import current_app, g, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, DateTime, or_, Column,ARRAY,Boolean

from flask_pymongo import PyMongo

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def get_mongo() -> Optional[PyMongo]:
    if 'mongo' not in g:
        mongo = PyMongo(current_app)
        g.mongo = mongo
    return g.mongo

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
    mongo = g.pop('mongo', None)
    # if mongo is not None:
    #     mongo.db.close()


alchemy = SQLAlchemy()
DbModel  = alchemy.Model
dbSession = alchemy.session
DbColumn = Column
DbInteger = Integer
DbString = String
DbDateTime = DateTime
db_or = or_
DbArray = ARRAY
DbBoolean = Boolean


def init(app: Flask):
    # log.i('flask env : {}'.format(app.config['SECRET_KEY']))
    app.config.from_mapping(SECRET_KEY='dev' if not app.config['SECRET_KEY'] else app.config['SECRET_KEY'],
                            DATABASE=os.path.join(app.instance_path, 'app.sqlite'))
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.instance_path}/app.sqlite'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    alchemy.init_app(app)
    # tells Flask to call that function
    # when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    with app.app_context():
        # get_db()  # 提前连接数据库
        # get_mongo()  # 提前连接数据库
        alchemy.create_all()