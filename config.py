# 所有配置项环境变量优先级大于本文件，若配置了环境变量将忽略此文件的配置(注意：vercel 修改环境变量后需要重新部署)！
# 前面加 * 内容必须配置, 否则无法正常使用
# 不配置数据库的话也是可以使用的, 但是配置数据库后将支持:
# 1. 消息长度支持超过 1000, 否则消息内容将存储在 url 的参数中, 超过最大长度将截断
# 2. 消息发送统计, 字数统计, 时间统计等
import os
SYS_CONFIG = {
    # *系统访问地址, 最后不需要加【/】，环境变量 SYS_URL (如果是 Vercel 部署一般是 https://[你起的仓库名]-[你的vercel用户名].vercel.app 当然也可以部署完之后再改)
    "sys_url": "",
    # *API访问密钥, 请务必修改默认值, 系统认证的唯一方式，环境变量 API_SECRET
    "api_secret": "",
    # 数据库完整连接地址
    # mysql示例：mysql+mysqlconnector://[数据库用户名]:[数据库密码]@[数据库地址]:3306/[数据库名]?charset=utf8mb4
    # mongodb示例：mongodb+srv://[数据库用户名]:[数据库密码]@[数据库地址]/[数据库名]?retryWrites=true&w=majority
    "db_link": ""
}

WX_CONFIG = {
    # *企业ID，环境变量 CORP_ID
    "corp_id": "",
    # *企业密钥，环境变量 CORP_SECRET
    "corp_secret": "",
    # *应用ID，环境变量 AGENT_ID
    "agent_id": ""
}


# 忽略下面的部分


def get(key: str):
    value = os.getenv(key.upper())
    if value is None:
        key = key.lower()
        if key in WX_CONFIG:
            value = WX_CONFIG[key]
        if key in SYS_CONFIG:
            value = SYS_CONFIG[key]
    return value
