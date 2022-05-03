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
import pytz

Base = declarative_base()


def gen_safe_id():
    return uuid.uuid5(uuid.NAMESPACE_X500, '{}|{}|{}'.format(config.get('api_secret'), str(time.time()), time.perf_counter())).hex


class MongoDBMsg:
    def __init__(self, dic):
        self.safe_id = dic["safe_id"]
        self.title = dic["title"]
        self.content = dic["content"]
        self.time = dic["time"]+timedelta(hours=8)


class SafeId:
    def __init__(self, safe_id):
        self.safe_id = safe_id


class MongoDBOp:
    def __init__(self):
        print("MongoDB初始化")
        conn_info = config.get('db_link')
        client = pymongo.MongoClient(
            conn_info, serverSelectionTimeoutMS=5000)
        db = client['wpush']
        self.col = db['message_detail']

    def insert_message(self, title, content):
        print("MongoDB插入")
        safe_id = gen_safe_id()
        message = {"safe_id": safe_id, "title": title,
                   "content": content, "time": datetime.now()}
        self.col.insert_one(message)
        return SafeId(safe_id)

    def query_message(self, msg_id):
        print("MongoDB查询消息")
        query = {"safe_id": msg_id}
        res = self.col.find_one(query)
        print("MongoDB查询结果", res)
        if res:
            return MongoDBMsg(res)
        else:
            return None


class MysqlMsg(Base):
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


class MysqlOp:
    def __init__(self):
        print("Mysql初始化")
        conn_info = config.get('db_link')
        engine = create_engine(conn_info, echo=True)
        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)
        self.session = session()

    def insert_message(self, title, content):
        print("Mysql插入消息")
        msg = MysqlMsg(title, content)
        self.session.add(msg)
        self.session.commit()
        return msg

    def query_message(self, msg_id):
        print("Mysq查询消息")
        return self.session.query(MysqlMsg).filter(MysqlMsg.safe_id == msg_id).one_or_none()

    def __del__(self):
        self.session.close()
