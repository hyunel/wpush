class YunError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class ApiError(YunError):
    def __init__(self, msg):
        super(ApiError, self).__init__(-2000, msg if msg else '请求上游API失败, 请检查配置文件')


class BadRequestError(YunError):
    def __init__(self, msg):
        super(BadRequestError, self).__init__(-1000, msg if msg else '非法请求')


class MissingParamError(YunError):
    def __init__(self, arg_name):
        super(MissingParamError, self).__init__(-1001, '缺少请求参数: %s' % arg_name)

