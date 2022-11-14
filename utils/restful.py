from flask import jsonify


class HttpCode(object):
    # 响应正常
    ok = 200
    # 没有登录错误
    unlogin_error = 401
    # 权限错误
    permission_error = 403
    # 参数错误
    param_error = 400
    # 服务器错误
    sever_error = 500


def _restful_result(code, message, data):
    return jsonify({'message': message or "", "data": data or {}}), code


def ok(message=None, data=None):
    return _restful_result(code=HttpCode.ok, message=message, data=data)


def unlogin_error(message='没有登录'):
    return _restful_result(code=HttpCode.unlogin_error, message=message, data=None)


def permission_error(message='没有权限访问'):
    return _restful_result(code=HttpCode.permission_error, message=message, data=None)


def param_error(message='参数错误'):
    return _restful_result(code=HttpCode.param_error, message=message, data=None)


def sever_error(message='服务器开小差啦'):
    return _restful_result(code=HttpCode.sever_error, message=message or '服务器内部错误', data=None)
