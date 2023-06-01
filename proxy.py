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


def launch_parser(pack_data):
    process = subprocess.Popen(["python", "parse.py"], stdin=subprocess.PIPE)
    process.stdin.write(pack_data + b'\r\n')
    process.stdin.close()


class NetInfo(object):

    @staticmethod
    def get_port():
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
    def __init__(self, data):
        self.__parse(data)

    def __parse(self, data: bytes):
        """Parse a HTTP request packet

        Args:
            data (bytes): Raw data
        """
        i0 = data.find(b'\r\n')  # Sep between line and header
        i1 = data.find(b'\r\n\r\n')  # Sep between header and data

        # Request Line
        self.req_line = data[:i0]
        self.method, self.req_uri, self.version = self.req_line.split()  # method, request uri, version

        # Request Header Fields
        self.req_header = data[i0 + 2:i1]
        self.headers = {}
        for header in self.req_header.split(b'\r\n'):
            k, v = header.split(b': ')
            self.headers[k] = v
        self.host = self.headers.get(b'Host')

        # Request data
        self.req_data = data[i1 + 4:]

class SimpleHttpProxy(object):
    def __init__(self, host: str='0.0.0.0', port: int=8080, listen: int=10, bufsize: int=8, delay: int=1):
        """Initialize sockets.

        Args:
            host (str, optional): Listening addr. Defaults to '0.0.0.0'.
            port (int, optional): Listening port. Defaults to 8080.
            listen (int, optional): Number of listening sockets. Defaults to 10.
            bufsize (int, optional): bufsize Buffer length (kb). Defaults to 8.
            delay (int, optional): delay Delay time (ms). Defaults to 1.
        """
        self.socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_proxy.bind((host, port))
        self.socket_proxy.listen(listen)

        self.socket_recv_bufsize = bufsize * 1024
        self.delay = delay / 1000.0

        print('\033[0;36mProxy launched!\033[0m')
        print(f'Listening {host}:{port}...')

    def __del__(self):
        self.socket_proxy.close()

    def __connect(self, host: str | bytes, port: int) -> socket.socket:
        """Parse DNS to get addr of the socket and build connection accordingly.

        Args:
            host (str | bytes): Host addr.
            port (int): Port.

        Returns:
            socket.socket: The socket constructed.
        """
        (family, sockettype, _, _, target_addr) = socket.getaddrinfo(host, port)[0]

        tmp_socket = socket.socket(family, sockettype)
        tmp_socket.setblocking(0)
        tmp_socket.settimeout(5)
        tmp_socket.connect(target_addr)
        return tmp_socket

    def __proxy(self, socket_client: socket.socket):
        """Core module of proxy.

        Args:
            socket_client (socket.socket): The socket between proxy and client.
        """

        req_data = socket_client.recv(self.socket_recv_bufsize)
        if req_data == b'':
            return

        http_packet = HttpRequestPacket(req_data)

        if b':' in http_packet.host:
            server_host, server_port = http_packet.host.split(b':')
        else:
            server_host, server_port = http_packet.host, 80

        # tmp = b'%s//%s' % (http_packet.req_uri.split(b'//')[0], http_packet.host)
        # req_data = req_data.replace(tmp, b'')
        if http_packet.method == b'POST' and http_packet.req_uri.startswith(b'http://mail.qq.com/cgi-bin/compose_send'):
            print(f'Webmail packet detected!\nClient IP address: {socket_server.getsockname()[0]}')
            launch_parser(req_data)

        # HTTP
        if http_packet.method in [b'GET', b'POST', b'PUT', b'DELETE', b'HEAD']:
            socket_server = self.__connect(server_host, server_port)
            socket_server.send(req_data)

        # HTTPS
        elif http_packet.method == b'CONNECT':
            socket_server = self.__connect(server_host, server_port)

            success_msg = b'%s %d Connection Established\r\nConnection: close\r\n\r\n' \
                          % (http_packet.version, 200)
            socket_client.send(success_msg)

            req_data = socket_client.recv(self.socket_recv_bufsize)
            socket_server.send(req_data)

        self.__nonblocking(socket_client, socket_server)

    def __nonblocking(self, socket_client: socket.socket, socket_server: socket.socket):
        """Process data (async).

        Args:
            socket_client (socket.socket): Socket between proxy and client.
            socket_server (socket.socket): Socket between proxy and server.
        """
        _rlist = [socket_client, socket_server]
        is_recv = True
        while is_recv:
            try:
                rlist, _, elist = select.select(_rlist, [], [], 2)
                if elist:
                    break
                for tmp_socket in rlist:
                    is_recv = True
                    data = tmp_socket.recv(self.socket_recv_bufsize)
                    if data == b'':
                        is_recv = False
                        continue

                    if tmp_socket is socket_client:
                        socket_server.send(data)
                        if data.startswith(b'POST http://mail.qq.com/cgi-bin/compose_send'):
                            print(f'Webmail packet detected!\nClient IP address: {socket_server.getsockname()[0]}')
                            launch_parser(data)

                    elif tmp_socket is socket_server:
                        socket_client.send(data)

                time.sleep(self.delay)
            except Exception as e:
                break

        socket_client.close()
        socket_server.close()

    def client_socket_accept(self):
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
    # Cmd Args
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
        sys.exit()

    # Launch
    SimpleHttpProxy(host, port, listen, bufsize, delay).start()
