from sqlalchemy import create_engine, Column, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import sessionmaker

import config
import uuid
import time

Base = declarative_base()


def gen_safe_id():
    return uuid.uuid5(uuid.NAMESPACE_X500, '{}|{}|{}'.format(config.get('api_secret'), str(time.time()), time.perf_counter())).hex


class Message(Base):
    __tablename__ = 'detail_message'  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)
    safe_id = Column(String(40), index=True, unique=True, nullable=False, default=gen_safe_id)
    title = Column(String(255), nullable=False)
    content = Column(MEDIUMTEXT(), nullable=False)
    time = Column(DateTime(), server_default=text('NOW()'))

    def __init__(self, title, content):
        self.title = title
        self.content = content


class Db:
    def __init__(self):
        conn_info = "mysql+mysqlconnector://%s:%s@%s:3306/%s?charset=utf8mb4" % \
                    (config.get('db_user'), config.get('db_pwd'), config.get('db_addr'), config.get('db_name'))

        engine = create_engine(conn_info, echo=True)
        Base.metadata.create_all(engine)

        session = sessionmaker(bind=engine)
        self.session = session()

    def insert_message(self, title, content):
        msg = Message(title, content)
        self.session.add(msg)
        self.session.commit()
        return msg

    def query_message(self, msg_id):
        return self.session.query(Message).filter(Message.safe_id == msg_id).one_or_none()

    def __del__(self):
        self.session.close()
