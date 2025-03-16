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

    def __init__(self, target_ip, target_port, protocol, udp_size_bytes=1024, thread_number=4):
        self.target_ip = target_ip
        self.target_port = target_port
        self.protocol = protocol
        self.udp_size_bytes = udp_size_bytes
        self.thread_number = thread_number

    def tcp_flood(self):
        return

    def start_attack(self):
        """
        Manage threads and choose attack method
        """
        threads = []
        try:
            for _ in range(self.thread_number):
                if self.protocol != False and self.protocol != '':
                    thread = Thread(target=self.tcp_flood())
                else:
                    print('Bad method')
                    return

        except Exception as e:
            color_text('red', f'[!] Error: {e}')
