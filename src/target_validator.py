import socket
from src.utils import color_text


class TargetValidator():
    def __init__(self, args):
        self.target = args.target
        self.verbose = args.verbose

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
        if self.verbose:
            color_text("green", f"[+] Trying to contact {self.target}")

            # If ip format
        if self.is_valid_ip():
            if self.verbose:
                color_text("green", f"[+] {self.target} is valide !\n")
            return True
        else:
            # if hostname format, trying to get ip or dns
            if self.is_valid_hostname():
                if self.verbose:
                    color_text("green", f"[+] {self.target} is valide !\n")
                return True
            else:
                color_text("red", f"[-] Impossible to contact {self.target}\n")
                return False
