import json
import time
import requests

import config
from errors import ApiError


class WxApi:
    cached_token = {}

    def get_token(self):
        if 'exp' in self.cached_token and self.cached_token['exp'] > time.time():
            return self.cached_token['token']

        ret = json.loads(requests.get('https://qyapi.weixin.qq.com/cgi-bin/gettoken', params={
            'corpid': config.get('corp_id'),
            'corpsecret': config.get('corp_secret')
        }).text)

        if ret['errcode'] != 0:
            raise ApiError(ret['errmsg'])

        self.cached_token['exp'] = time.time() + ret['expires_in']
        self.cached_token['token'] = ret['access_token']
        return ret['access_token']

    def send_msg(self, msg_type, msg_content, user='@all', party='', tag='', safe=0, dup_check=0, dup_check_interval=1800):
        data = {
            'safe': safe,
            'touser': user,
            'toparty': party,
            'totag': tag,
            'msgtype': msg_type,
            'agentid': config.get('agent_id'),
            'enable_duplicate_check': dup_check,
            'duplicate_check_interval': dup_check_interval,
            msg_type: msg_content
        }

        ret = json.loads(requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send', params={
            "access_token": self.get_token()
        }, json=data).text)

        if ret['errcode'] != 0:
            raise ApiError(ret['errmsg'])
        
    def send_text_card(self, title, description, url, btn_txt='详情', **kwargs):
        self.send_msg('textcard', {
                      'title': title, 'description': description, 'url': url, 'btntxt': btn_txt}, **kwargs)

    def send_news(self, title, description, url, pic, **kwargs):
        self.send_msg('news', {'articles': [
                      {'title': title, 'description': description, 'url': url, 'picurl': pic}]}, **kwargs)
