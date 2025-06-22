import multiprocessing
import socket

CPU_COUNT = multiprocessing.cpu_count()

DEFAULT_NUM_THREADS = 100

TCP = socket.SOCK_STREAM
UDP = socket.SOCK_DGRAM
