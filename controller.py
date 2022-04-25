import json
import time
from urllib.parse import quote

from db import Db
import config
from wx_api import WxApi
from errors import *
import render
import requests

DB = Db() if config.get('db_addr') != '' and config.get('db_name') != '' else None
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

        if type(to_user) is list:
            to_user = '|'.join(to_user)
        if type(to_tag) is list:
            to_tag = '|'.join(to_tag)
        if type(to_party) is list:
            to_party = '|'.join(to_party)

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
        return {"body": "WPush 已成功搭建~"}

    def send_msg(self):
        # TODO 更多消息类型的支持
        type = self.get_param('type')
        title = self.get_param('title')
        content = self.get_param('content')
        pic = self.get_param('pic')
        summary = self.get_param('summary')
        url = self.get_param('url')
        if not type:
            type = "text"
        if not content:
            content = "No Content"
        if not summary:
            summary = content[:128] + '...' if len(content) > 128 else content
        if not pic and type == "news":
            pic = get_bing()
        print('url1')
        print(url)

        # 数据库部分待测试
        if DB:
            msg = DB.insert_message(title, content)
            if type == "textcard" or type == "news":
                if not url:
                    url = '{}/show/{}'.format(config.get('sys_url'),
                                              msg.safe_id)
            if type == "text":
                WX_API.send_text(msg.content, **self.spec_send_to())
            elif type == "markdown":
                WX_API.send_markdown(msg.content, **self.spec_send_to())
            elif type == "textcard":
                WX_API.send_text_card(msg.title, summary, url,
                                      **self.spec_send_to())
            elif type == "news":
                WX_API.send_news(msg.title, summary, url, pic,
                                 **self.spec_send_to())
            return {"body": {"code": 0, "msg_id": msg.safe_id}}
        else:
            if type == "textcard" or type == "news":
                if not url:
                    url = '{}/show?t={}&h={}&c={}'.format(
                        config.get('sys_url'),
                        int(time.time()*1000),
                        quote(title, encoding='utf-8'),
                        quote(content, encoding='utf-8')[:1900])
            print('url2')
            print(url)
            if type == "text":
                self.verify_params('content')
                WX_API.send_text(content, **self.spec_send_to())
            elif type == "markdown":
                self.verify_params('content')
                WX_API.send_markdown(content, **self.spec_send_to())
            elif type == "textcard":
                self.verify_params('title')
                self.verify_params('content')
                WX_API.send_text_card(
                    title, summary, url, **self.spec_send_to())
            elif type == "news":
                self.verify_params('title')
                WX_API.send_news(title, summary, url, pic,
                                 **self.spec_send_to())
            return {"body": {"code": 0}}

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
