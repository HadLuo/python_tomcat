from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from tomcat.http_bodys import *
import traceback
import importlib


class HttpControllerContext:

    def __init__(self):
        Log.i("负责controller处理的处理器初始化完成！")

    def find_static(self, request):
        # 项目路径
        root = Global.get_instance().get_project_path()
        url = request.get_url().replace("//", "")
        # 本地資源路徑
        res_path = root + Global.file_separator + url[url.find("/") + 1:]
        if not os.path.exists(res_path):
            # 文件不存在 ，返回404
            return HttpResponse.build404(request, res_path)
        try:
            return HttpResponse.build200(request, File.read_string(res_path))
        except:
            traceback.print_exc()
            return HttpResponse.build500(request, traceback.format_exc())

    def find_script(self, request):
        server_yml = Global.get_instance().get_server_yml()
        # 是controller , 执行python脚本
        scripts = Global.get_instance().get_project_path() + Global.file_separator + server_yml['controller-dir']
        # 获取脚本文件
        pys = File.list_files(scripts, ['py'])
        # 找到脚本文件
        root = Global.get_instance().get_project_path()
        url = request.get_url().replace("//", "")
        if "?" in url:
            url = url[:url.find('?')]
        if request.get_url_suffix():
            url = url.replace("." + request.get_url_suffix(), ".py")
        else:
            url = url + ".py"
        # 本地資源路徑
        res_path = root + Global.file_separator + url[url.find("/") + 1:]
        if not os.path.exists(res_path):
            # 文件不存在 ，返回404
            return HttpResponse.build404(request, res_path)
        try:
            # 执行python代码
            model_name = res_path.replace(root, "").replace(Global.file_separator, ".").replace('/', '.').replace('.py',
                                                                                                                  '')
            if model_name.startswith('.'):
                model_name = model_name[1:]
            Log.i("start exec python script >> model=" + model_name)
            module_object = importlib.import_module(model_name)  # 将模块加载为对象
            importlib.reload(module_object)
            ret = module_object.service(request)
            return HttpResponse.build200(request, ret)
        except:
            traceback.print_exc()
            return HttpResponse.build500(request, traceback.format_exc())

    def call_function(self, obj, function_name, *args, **kwargs):
        result = obj.__getattribute__(function_name)(*args, **kwargs)
        return result

    def do_action(self, http_request):
        server_yml = Global.get_instance().get_server_yml()
        # 服务器支持的动态脚本后缀
        suffixs = server_yml['controller-suffix']
        # 判断是否是动态脚本
        suffix = http_request.get_url_suffix()
        print(suffix)
        if not suffix or suffix in suffixs:
            #  动态脚本文件
            return self.find_script(http_request)
        # 静态文件
        return self.find_static(http_request)


class Empty:
    def __init__(self):
        pass


class HttpHandler:

    def __init__(self):
        server_yml = Global.get_instance().get_server_yml()
        max_workers = server_yml['handler-threadpool']['max_workers']
        # 表示在这个线程池中同时运行的线程有max_workers个线程
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        Log.i("负责处理数据分发的处理器初始化完成！max_workers=" + str(max_workers))
        self.controller = HttpControllerContext()

    def __dowork(self, socket_info):
        try:
            # 取出数据，这里需要优化!!!!!
            datas = socket_info.get_socket().recv(1024 * 4)
            if not datas:
                Log.i("socket datas empty :" + socket_info.get_addr())
            # 构造控制器 处理
            response = self.controller.do_action(HttpRequest(str(datas, "utf-8"), socket_info))
            # 回送socket信息
            socket_info.get_socket().send(bytes(response.get_response(), encoding="utf8"))
            # 关闭socket
            socket_info.get_socket().close()
            Log.i("shutdown socket >> " + str(socket_info.get_addr()))
        except:
            traceback.print_exc()

    def handle(self, socket_info):
        self.executor.submit(self.__dowork, socket_info)
