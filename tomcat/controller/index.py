from tomcat.controller.postman import *


def service(request):
    body = request.body()
    print("收到index请求,p:" + str(body))
    return {'code': 0, 'data': '请求成功'}
