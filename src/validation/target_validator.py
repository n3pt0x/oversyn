from src.config import Config
import socket


class TargetValidator():
    def __init__(self, target):
        self.target = target

    def is_valid_ip(self):
        """Return if the name of the target is valid as an IP address (IPv4 or IPv6)"""
        try:
            if socket.inet_pton(socket.AF_INET, self.target):
                return True
            elif socket.inet_pton(socket.AF_INET6, self.target):
                return True
        except:
            return False

    def is_valid_hostname(self):
        """Verified if hostname is valid by resolving it to an IP address"""
        try:
            socket.gethostbyname(self.target)
            return True
        except:
            return False

    def validate(self):
        """Return if target is valide"""
        if Config.get_verbose():
            print(f"Trying to contact {self.target} ...\n")

            # If ip format
        if self.is_valid_ip():
            if Config.get_verbose():
                print(f'{self.target} is valide !')
            return True
        else:
            # if hostname format, trying to get ip or dns
            if self.is_valid_hostname():
                if Config.get_verbose():
                    print(f'{self.target} is valide !')
                return True
            else:
                print(f"Impossible to contact {self.target} ...")
                return False
