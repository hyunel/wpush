# 前面加 * 内容必须配置, 否则无法正常使用
# 不配置数据库的话也是可以使用的, 但是配置数据库后将支持:
# 1. 消息长度支持超过 1000, 否则消息内容将存储在 url 的参数中, 超过最大长度将截断
# 2. 消息发送统计, 字数统计, 时间统计等
SYS_CONFIG = {
    # *系统访问地址, 最后不需要加【/】
    "sys_url": "https://service-xxxxx-xxxxx.xxxxx.apigw.tencentcs.com",
    # *API访问密钥, 请务必修改默认值, 系统认证的唯一方式
    "api_secret": "XXXXXXXXXXXXXXXX",
    # MYSQL 数据库地址
    "db_addr": "",
    # 数据库用户名
    "db_user": "wxpush",
    # 数据库密码
    "db_pwd": "",
    # 数据库名
    "db_name": "wxpush"
}

WX_CONFIG = {
    # *企业ID
    "corp_id": "",
    # *企业密钥
    "corp_secret": "",
    # *应用ID
    "agent_id": ""
}