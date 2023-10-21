import json
from urllib.parse import parse_qs

import controller
import route
from errors import YunError

route = route.setup_routes()


# 阿里云 HTTP 触发器
def handler(environ, start_response):
    route_result = route.match(environ['fc.request_uri'], environ['REQUEST_METHOD'])
    if route_result is None:
        start_response('404 Not Found', [])
        return []

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        request_body = environ['wsgi.input'].read(request_body_size)
        if type(request_body) is bytes:
            request_body = request_body.decode(encoding='utf8')
    except ValueError:
        request_body = None

    try:
        query_string = parse_qs(environ['QUERY_STRING'])
        for key in query_string:
            if len(query_string[key]) == 1:
                query_string[key] = query_string[key][0]

        obj = controller.MainController({
            'body': request_body,
            'queryString': query_string
        }, route_result)
        result = getattr(obj, route_result['action'])()
    except YunError as e:
        start_response('500 Internal Server Error', [('Content-type', 'application/json;charset=utf-8')])
        return [json.dumps({"code": e.code, "msg": e.message}, ensure_ascii=False)]

    if 'body' in result and type(result['body']) is str:
        start_response('200 OK', [('Content-type', 'text/html;charset=utf-8')])
        return [result['body']]

    resp = {"code": 0, "msg": None}
    start_response('200 OK', [('Content-type', 'application/json;charset=utf-8')])
    if 'body' in result and type(result['body']) is dict:
        resp.update(result['body'])
    return [json.dumps(resp, ensure_ascii=False)]


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
