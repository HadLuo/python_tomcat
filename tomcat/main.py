from tomcat.sockets import *

ServerSockets(Global.get_instance().get_server_yml()['port']).startup()
