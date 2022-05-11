import json
import time
from urllib.parse import quote

from db import get_db
import config
from wx_api import WxApi
from errors import *
import render
import requests

DB = get_db()
WX_API = WxApi()


def get_bing():
    bing_url = "https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
    res = requests.get(bing_url).json()
    bing_pic = "https://cn.bing.com/"+res["images"][0]["url"]
    return bing_pic


class MainController:
    def __init__(self, event, route_result):
        self.event = event
        self.route_result = route_result

        try:
            if 'body' in self.event and self.event['body'] != '':
                self.event['body'] = json.loads(self.event['body'])
            else:
                self.event['body'] = {}
        except json.decoder.JSONDecodeError:
            raise BadRequestError('请求数据非法')

        if route_result['secret'] and self.get_param('secret') != config.get('api_secret'):
            raise BadRequestError('请求密钥不正确')

    def get_param(self, name, default=None):
        if name in self.event['queryString'] and self.event['queryString'][name]:
            return self.event['queryString'][name]
        if name in self.event['body'] and self.event['body'][name]:
            return self.event['body'][name]
        return default

    def verify_params(self, *args):
        for arg in args:
            if arg not in self.event['body'] and arg not in self.event['queryString']:
                raise MissingParamError(arg)

    def spec_send_to(self):
        ret = {}
        to_user = self.get_param('to')
        if self.get_param('user'):
            to_user = self.get_param('user')
        to_tag = self.get_param('tag')
        to_party = self.get_param('party')

        if type(to_user) is list:
            to_user = '|'.join(to_user)
        if type(to_tag) is list:
            to_tag = '|'.join(to_tag)
        if type(to_party) is list:
            to_party = '|'.join(to_party)

        if to_tag or to_party:
            ret['user'] = ''    # 删除默认值
        elif to_user:
            ret['user'] = to_user
        if to_tag:
            ret['tag'] = to_tag
        if to_party:
            ret['party'] = to_party
        return ret

    def index(self):
        # TODO 主页渲染
        return {"body": render.show_index()}

    def send_msg(self):
        resp = {"body": {"code": 0}}
        msg_type = self.get_param('type')

        # 有标题默认发卡片消息，没有标题发普通文本消息
        if msg_type is None and self.get_param('content'):
            msg_type = 'text'
            if self.get_param('title'):
                msg_type = 'textcard'

        if msg_type is None:
            raise BadRequestError('请提供消息内容(content) 或指定消息类型(type)')

        if msg_type == "textcard" or msg_type == "news":
            self.verify_params('title', 'content')

            url = self.get_param('url')
            title = self.get_param('title')
            content = self.get_param('content')
            summary = self.get_param(
                'summary', default=content[:128] + '...' if len(content) > 128 else content)
            print("内容", content)
            if not url:
                if DB:
                    msg = DB.insert_message(title, content)
                    url = '{}/show/{}'.format(config.get('sys_url'),
                                              msg.safe_id)
                    resp['body']['msg_id'] = msg.safe_id
                else:
                    url = '{}/show?t={}&h={}&c={}'.format(
                        config.get('sys_url'),
                        int(time.time()*1000),
                        quote(title, encoding='utf-8'),
                        quote(content, encoding='utf-8')[:1900])
            resp['body']['link'] = url
            if msg_type == "news":
                pic = self.get_param('pic', default=get_bing())
                WX_API.send_news(title, summary, url, pic,
                                 **self.spec_send_to())

            if msg_type == 'textcard':
                WX_API.send_text_card(
                    title, summary, url, **self.spec_send_to())
        else:
            params = {}
            params.update(self.event['queryString'])
            params.update(self.event['body'])

            WX_API.send_msg(msg_type, params, **self.spec_send_to())

        return resp

    def show_msg(self):
        if not DB:
            raise BadRequestError("请先配置数据库")
        msg = DB.query_message(self.route_result['params']['msg_id'])
        if msg:
            return {"body": render.show(msg.title, msg.content, msg.time.strftime("%Y-%m-%d %H:%M:%S"))}
        else:
            raise BadRequestError("没有这篇文章")

    def show_msg_param(self):
        self.verify_params('t', 'h', 'c')
        return {"body": render.show_param()}
