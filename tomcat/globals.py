import os
from tomcat.tools import *


class Global:
    instance = None
    # 文件分隔符
    file_separator = "\\"
    # 換行
    line_separator = "\r\n"
    # 空格
    space = " "

    def __init__(self):
        # 当前项目目录
        self.project_path = os.path.abspath(os.curdir)
        # 读取配置
        self.server_yml = File.read_yml(self.project_path + Global.file_separator + "server.yml")

    def get_server_yml(self):
        return self.server_yml

    def get_project_path(self):
        return self.project_path

    @staticmethod
    def get_instance():
        if not Global.instance:
            Global.instance = Global()
        return Global.instance
