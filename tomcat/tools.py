import yaml
import os
import json


class Url:

    # 解析url参数 ，变成字典
    @staticmethod
    def parse_url_param(url):
        if '?' in url:
            temp_url = url[url.find('?'):]
            if temp_url == "?":
                return {}
            temp_url = temp_url[1:]
            if '&' not in temp_url:
                if '=' in temp_url:
                    a = temp_url.split('=')
                    if len(a) != 2:
                        return {}
                    return {a[0]: a[1]}
            else:
                ass = temp_url.split('&')
                ret = {}
                for a in ass:
                    if '=' in a:
                        b = a.split('=')
                        if len(b) != 2:
                            continue
                        ret[b[0]] = b[1]
                return ret
            return {}


# 日志
class Log:
    @staticmethod
    def i(msg):
        print(msg)


# 文件
class File:
    # 加载 yml ,返回字典类型
    @staticmethod
    def read_yml(yaml_path):
        f = open(yaml_path, 'r', encoding='utf-8')
        return yaml.load(f.read(), Loader=yaml.FullLoader)

    # 递归遍历文件， suffixs 为要获取的 文件后缀
    @staticmethod
    def list_files(file_dir, suffixs=[]):
        ret = []
        for home, dirs, files in os.walk(file_dir):
            for filename in files:
                fullname = os.path.join(home, filename)
                if fullname:
                    if suffixs:
                        for su in suffixs:
                            if fullname.endswith(su):
                                ret.append(fullname)
                    else:
                        ret.append(fullname)
        return ret

    # 读文件 变成json格式
    @staticmethod
    def read_json(file_path):
        with open(file_path, "r", encoding='UTF-8') as f:
            return json.load(f)

    # 读文件 变成 string
    @staticmethod
    def read_string(file_path):
        ret = ""
        with open(file_path, "r", encoding='UTF-8') as f:
            for line in f.readlines():
                ret = ret + line + "\r\n"
            return ret
