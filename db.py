from sqlalchemy import create_engine, Column, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import pymongo
import config
import uuid
import time


def get_db():
    db_type = config.get('db_link').split('+')[0]
    if db_type == 'mysql':
        return MysqlDB()
    elif db_type == 'mongodb':
        return MongoDB()
    else:
        return None


def gen_safe_id():
    return uuid.uuid5(uuid.NAMESPACE_X500, '{}|{}|{}'.format(config.get('api_secret'), str(time.time()), time.perf_counter())).hex


class MongoDB:
    class Message:
        def __init__(self, dic):
            self.safe_id = dic["safe_id"]
            self.title = dic["title"]
            self.content = dic["content"]
            self.time = dic["time"] + timedelta(hours=8)

    def __init__(self):
        conn_info = config.get('db_link')
        client = pymongo.MongoClient(
            conn_info, serverSelectionTimeoutMS=5000)
        db = client['wpush']
        self.col = db['message_detail']

    def insert_message(self, title, content):
        safe_id = gen_safe_id()
        message = {"safe_id": safe_id, "title": title,
                   "content": content, "time": datetime.now()}
        self.col.insert_one(message)
        return self.Message(message)

    def query_message(self, msg_id):
        query = {"safe_id": msg_id}
        res = self.col.find_one(query)
        if res:
            return self.Message(res)
        else:
            return None


class MysqlDB:
    Base = declarative_base()

    class Message(Base):
        __tablename__ = 'detail_message'  # 表名
        id = Column(Integer, primary_key=True, autoincrement=True)
        safe_id = Column(String(40), index=True, unique=True,
                         nullable=False, default=gen_safe_id)
        title = Column(String(255), nullable=False)
        content = Column(MEDIUMTEXT(), nullable=False)
        time = Column(DateTime(), server_default=text('NOW()'))

        def __init__(self, title, content):
            self.title = title
            self.content = content

    def __init__(self):
        conn_info = config.get('db_link')
        engine = create_engine(conn_info, echo=True)
        self.Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)
        self.session = session()

    def insert_message(self, title, content):
        msg = self.Message(title, content)
        self.session.add(msg)
        self.session.commit()
        return msg

    def query_message(self, msg_id):
        return self.session.query(self.Message).filter(self.Message.safe_id == msg_id).one_or_none()

    def __del__(self):
        self.session.close()
