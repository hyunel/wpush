import re
from urllib.parse import urlparse


# 丐版路由
class Router:
    rules = []

    def add(self, uri, action, methods=None, secret=False):
        self.rules.append({'uri': uri, 'action': action, 'methods': methods, 'secret': secret})

    def match(self, url, method='GET'):
        for rule in self.rules:
            if rule['methods'] and method not in rule['methods']:
                continue
            needle = [x for x in rule['uri'].split('/') if x]
            path = [x for x in urlparse(url).path.split('/') if x]
            if len(needle) != len(path):
                continue

            flag_matched = True
            matched_params = {}
            for index, unit in enumerate(needle):
                if unit[:1] == '{' and unit[-1:] == '}':
                    pos = unit.find(':')
                    match = re.match('(%s)' % unit[pos+1:-1], path[index])
                    if not match:
                        flag_matched = False
                        break
                    matched_params[unit[1:pos]] = match[1]
                else:
                    if path[index] != unit:
                        flag_matched = False
                        break

            if flag_matched:
                return {'action': rule['action'], 'params': matched_params, 'secret': rule['secret']}
        return


def setup_routes():
    # 设置路由
    route = Router()
    route.add(R'/show/{msg_id:[0-9a-z\-]+}', action='show_msg', methods=["GET"])
    route.add(R'/show', action='show_msg_param', methods=["GET"])
    route.add('/send', action='send_msg', methods=["GET", "POST"], secret=True)
    route.add('/', action='index')
    return route
