import json

import route
import controller
from errors import YunError

route = route.setup_routes()


# 腾讯 API 网关触发器
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
            obj = controller.MainController(event, route_result)
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
