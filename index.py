import json

import route
import controller
from errors import YunError

# 设置路由
route = route.Router()
route.add(R'/show/{msg_id:[0-9a-z\-]+}', action='show_msg', methods=["GET"])
route.add(R'/show', action='show_msg_param', methods=["GET"])
route.add('/send', action='send_msg', methods=["GET", "POST"], secret=True)
route.add('/send_rich', action='send_rich_msg', methods=["POST"], secret=True)
route.add('/', action='index')


# API 网关触发器
def main_handler(event, context):
    event_result = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {}
    }
    route_result = route.match(event['path'], event['httpMethod'])
    if route_result is None:
        event_result['statusCode'] = 404
        event_result['body'] = '404 Not Found'
    else:
        try:
            obj = controller.MainController(event, context, route_result)
            event_result.update(getattr(obj, route_result['action'])())
        except YunError as e:
            event_result['statusCode'] = 500
            event_result['body'] = {"code": e.code, "msg": e.message}

    if type(event_result['body']) is dict:
        event_result['headers']['Content-Type'] = 'application/json;charset=utf-8'
        event_result['body'] = json.dumps(event_result['body'], ensure_ascii=False)
    else:
        event_result['headers']['Content-Type'] = 'text/html;charset=utf-8'

    return event_result
