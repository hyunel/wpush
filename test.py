import json

from index import main_handler
import config


# 普通消息发送测试
print(main_handler({
    "path": "/send",
    "httpMethod": "POST",
    "queryString": {
        "secret": config.get('api_secret'),
        "title": "dbg---OK"
    }
}, None))

# 卡片消息发送测试
result = main_handler({
    "path": "/send",
    "httpMethod": "POST",
    "queryString": {
        "secret": config.get('api_secret'),
        "title": "dbg---OK",
        "content": "这是卡片消息"
    }
}, None)
print(result)

# 消息读取测试
print(main_handler({
    "path": "/show/%s" % json.loads(result['body'])['msg_id'],
    "httpMethod": "GET",
    "queryString": {}
}, None))
