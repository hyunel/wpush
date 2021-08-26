import json
import time
from urllib.parse import quote

from db import Db
from config import WX_CONFIG, SYS_CONFIG
from wx_api import WxApi
from errors import *
import render

DB = Db() if SYS_CONFIG['db_addr'] != '' and SYS_CONFIG['db_name'] != '' else None
WX_API = WxApi(WX_CONFIG)


class MainController:
    def __init__(self, event, context, route_result):
        self.event = event
        self.context = context
        self.route_result = route_result

        try:
            if 'body' in self.event and self.event['body'] != '':
                self.event['body'] = json.loads(self.event['body'])
            else:
                self.event['body'] = {}
        except json.decoder.JSONDecodeError:
            raise BadRequestError('请求数据非法')

        if route_result['secret'] and self.get_param('secret') != SYS_CONFIG['api_secret']:
            raise BadRequestError('请求密钥不正确')

    def get_param(self, name):
        if name in self.event['queryString']:
            return self.event['queryString'][name]
        if name in self.event['body']:
            return self.event['body'][name]
        return None

    def verify_params(self, *args):
        for arg in args:
            if arg not in self.event['body'] and arg not in self.event['queryString']:
                raise MissingParamError(arg)

    def spec_send_to(self):
        ret = {}
        to_user = self.get_param('to')
        to_tag = self.get_param('tag')
        to_party = self.get_param('party')
        if to_tag or to_party:
            ret['to'] = ''    # 删除默认值
        elif to_user:
            ret['to'] = to_user
        if to_tag:
            ret['tag'] = to_tag
        if to_party:
            ret['party'] = to_party
        return ret

    def index(self):
        # TODO 主页渲染
        return {"body": "WxPush 已成功搭建~"}

    def send_msg(self):
        # TODO 更多消息类型的支持
        self.verify_params('tittle')
        tittle = self.get_param('tittle')
        content = self.get_param('content')
        if not content:
            WX_API.send_text(self.get_param('tittle'), **self.spec_send_to())
        else:
            summary = content[:128] + '...' if len(content) > 128 else content
            # 数据库已经正常配置
            if DB:
                msg = DB.insert_message(tittle, content)
                WX_API.send_text_card(msg.tittle, summary, '{}/show/{}'.format(SYS_CONFIG['sys_url'], msg.safe_id),
                                      **self.spec_send_to())
                return {"body": {"code": 0, "msg_id": msg.safe_id}}
            else:
                # content 放进 url 参数里, 长度超过 1000 则截断
                WX_API.send_text_card(tittle, summary, '{}/show?t={}&h={}&c={}'.format(
                    SYS_CONFIG['sys_url'],
                    int(time.time()*1000),
                    quote(tittle, encoding='utf-8'),
                    quote(content, encoding='utf-8')[:1900]), **self.spec_send_to())
        return {"body": {"code": 0}}

    def show_msg(self):
        if not DB:
            raise BadRequestError("请先配置数据库")
        msg = DB.query_message(self.route_result['params']['msg_id'])
        if msg:
            return {"body": render.show(msg.tittle, msg.content, msg.time.strftime("%Y-%m-%d %H:%M:%S"))}
        else:
            raise BadRequestError("没有这篇文章")

    def show_msg_param(self):
        self.verify_params('t', 'h', 'c')
        return {"body": render.show_param()}

    def send_rich_msg(self):
        self.verify_params('type', 'data')
        WX_API.send_msg(self.get_param('type'), self.get_param('data'), **self.spec_send_to())
        return {"body": {"code": 0}}
