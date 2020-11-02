import requests
import json


class PostMan:
    def __init__(self, token=None):
        debug = False
        if debug:
            print("请注意是测试环境")
            # 测试环境
            self.url = 'http://lk-nodejs-web.test.csbilin.com/java-gateway/sq-fg/'
        else:
            print("请注意是正式环境")
            # 正式环境
            self.url = 'https://web.bilinl.com/java-gateway/sq-fg/'
        self.cookie = {}
        self.headers = {}

    def set_token(self):
        login = 'https://web.bilinl.com/java-gateway/uaa/login/acct?clientId=83YslrcMpBt3X3c0eK8jvhdPAW84ScHc&clientSecret=rosJtPuAMy69wnEMiw9UqRaQNELypEyk&username=13467936875&password=123456abcd'
        ret = self.__post(login, {
            'username': '13467936875',
            'password': '123456abcd',
            'phoneLogin': 0,
            'clientId': '83YslrcMpBt3X3c0eK8jvhdPAW84ScHc',
            'clientSecret': 'rosJtPuAMy69wnEMiw9UqRaQNELypEyk'
        })
        print(str(json.loads(ret)))
        token = json.loads(ret)['data']['value']
        self.cookie = {
            'token': token
        }
        self.headers = {
            'Content-Type': 'application/json',
            'authorization': 'Bearer ' + token
        }
        print("获取到token>> " + token)
        return token

    def __post(self, url, data):
        response = requests.post(url, headers=self.headers, data=json.dumps(data), cookies=self.cookie)
        return response.text

    def redis(self, cmd, method='its/r'):
        args = cmd.split(' ')
        value = None
        if len(args) == 3:
            value = args[2]
        redis_data = {
            "op": args[0],
            'key': args[1],
            'value': value
        }
        return self.__post(self.url + method, redis_data)

    def sql(self, sql, method='its/sql'):
        if not sql:
            print("请输入sql")
            return
        if 'SELECT' in sql:
            print('占不支持查询语句，请到navicat执行')
            return
        sql_data = {
            'sql': sql
        }
        return self.__post(self.url + method, sql_data)
