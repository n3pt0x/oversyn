from src.config import Config
import argparse


class ArgParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="0verSyn",
            description="Tool for attack DoS.",
            epilog="Used the --help or -h flag for more information",
            usage="python main.py <target>"
        )

        self.parser.add_argument(
            "target",
            type=str,
            help="The IP address of the target"
        )

        self.parser.add_argument(
            "-p",
            "--port",
            type=int,
            help="Port of the target number"
        )

        self.parser.add_argument(
            "-c",
            "--count",
            type=int,
            default=None,
            help="Number of requests, default set on infinite"
        )

        self.parser.add_argument(
            "-a",
            "--attack",
            choices=['tcp', 'udp', 'http'],
            required=True,
            help="Choose the attack type: TCP or UDP flood, or HTTP"
        )

        self.parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Used the verbose mode"
        )

    def parse_args(self):
        """return args list"""
        return self.parser.parse_args()
