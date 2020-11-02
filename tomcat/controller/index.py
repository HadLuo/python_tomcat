from tomcat.controller.postman import *


def service(request):
    body = request.body()
    print("收到index请求,p:" + str(body))
    postman = PostMan()
    postman.set_token()
    if body['type'] == '0':
        ret = postman.redis(body['param'])
        return {'code': 0, 'data': ret}
    elif body['type'] == '1':
        ret = postman.sql(body['param'])
        return {'code': 0, 'data': ret}
    else:
        return {'code': -1, 'err': '不支持的操作'}
