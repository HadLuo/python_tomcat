from tomcat.globals import *


class HttpParser:

    def __init__(self):
        pass

    def parse(self, datas):
        result = {}
        # 按行 分隔
        lines = datas.split(Global.line_separator)

        lines_details = lines[0].split(Global.space)
        result['method'] = lines_details[0]
        result['url'] = lines_details[1]
        result['protocol'] = lines_details[2]

        lines_details = lines[3].split(Global.space)
        result['content_length'] = lines_details[1]

        lines_details = lines[4].replace('Accept: ', "").split(',')
        result['accept'] = lines_details

        # 最后一行 , 请求体内容
        result['body_json'] = lines[len(lines) - 1]
        return result


class HttpRequest:

    def __init__(self, datas, socket_info):
        self.datas = datas
        self.socket_info = socket_info
        # 方法名  GET POST
        self.method = None
        # 请求url
        self.url = None
        # 协议
        self.protocol = None
        self.accept = []
        # 请求体 数据的长度
        self.content_length = 0
        #  请求 参数
        self.body_param = {}
        # 解析器
        self.parser = HttpParser()
        # 解析http 请求基础内容
        self.__resolve_base()
        # 解析 请求参数
        self.__resolve_params()
        # 解析一些 其它的
        self.__resolve_extra()

    def __resolve_extra(self):
        if '?' in self.url:
            t = self.url[0:self.url.find('?')]
            t = t[t.rfind('/') + 1:]
            if '.' in t:
                self.suffix = t[t.rfind('.') + 1:]
            else:
                self.suffix = ""
        else:
            t = self.url[self.url.rfind('/') + 1:]
            if '.' in t:
                self.suffix = t[t.rfind('.') + 1:]
            else:
                self.suffix = ""
            # self.suffix = self.url[self.url.rfind('/') + 1:]

    def __resolve_params(self):
        # 解析 url上面的 参数
        if self.method == 'GET':
            # get请求参数在链接上
            self.body_param = Url.parse_url_param(self.url)
        elif self.method == 'POST':
            if '&' in self.body_param:
                ass = self.body_param.split('&')
                ret = {}
                for a in ass:
                    if '=' in a:
                        b = a.split('=')
                        if len(b) != 2:
                            continue
                        ret[b[0]] = b[1]
                self.body_param = ret
            else:
                self.body_param = json.loads(self.body_param)

    def __resolve_base(self):
        result = self.parser.parse(self.datas)
        self.method = result['method']
        self.url = result['url']
        self.protocol = result['protocol']
        self.content_length = result['content_length']
        self.body_param = result['body_json']
        self.accept = result['accept']
        Log.i("====================http request=======================")
        Log.i(self.datas)

    def body(self):
        return self.body_param

    def get_url_suffix(self):
        return self.suffix

    def get_url(self):
        return self.url

    def get_protocol(self):
        return self.protocol

    def get_accept(self):
        return self.accept


class HttpResponse:
    format = '''${protocol} ${code} ${code_hint}
Content-Type: ${content_type}
Connection: keep-alive
Keep-Alive: timeout=30
Access-Control-Allow-Origin: *
timing-allow-origin: *

${body}
    '''
    code_format = {
        '404': 'Not Found',
        '200': 'OK',
        '500': 'Server-Error',
    }

    def __init__(self, request, code, body):
        res = HttpResponse.format.replace('${protocol}', request.get_protocol())
        res = res.replace('${code}', str(code))
        res = res.replace('${code_hint}', HttpResponse.code_format[str(code)])
        res = res.replace('${content_type}', request.get_accept()[0])
        if body == None:
            body = ""
        if body.__class__ == {}.__class__:
            # 字典类型
            import json
            self.res = res.replace('${body}', json.dumps(body, ensure_ascii=False))
        else:
            self.res = res.replace('${body}', body)
        Log.i("====================http response=======================")
        Log.i(self.res)

    def get_response(self):
        return self.res

    @staticmethod
    def build404(request, path):
        return HttpResponse(request, 404, "Not Fond in Server! " + path)

    @staticmethod
    def build200(request, content):
        return HttpResponse(request, 200, content)

    @staticmethod
    def build500(request, err):
        return HttpResponse(request, 500, err)
