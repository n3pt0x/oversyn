import argparse
from src.config import DEFAULT_NUM_THREADS


def arg_parser():

    parser = argparse.ArgumentParser(
        prog="0verSyn",
        description="Tool for attack DoS.",
        epilog="Used the --help or -h flag for more information",
        usage="python main.py <target>"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Used the verbose mode"
    )

    parser.add_argument(
        "target",
        type=str,
        help="The IP address of the target"
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        required=True,
        help="Port of the target number"
    )

    parser.add_argument(
        "-a",
        "--attack",
        choices=['tcp', 'udp', 'http', 'https'],
        required=True,
        help="Choose the attack type: TCP or UDP flood, or HTTP(S)"
    )

    parser.add_argument(
        "-m",
        "--method",
        choices=['get', 'post'],
        type=str,
        help="Choise your HTTP method"
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=None,
        help="Number of requests, default set on infinite"
    )

    parser.add_argument(
        "-t",
        "--thread",
        type=int,
        default=None,
        help=f"Number of threads, default set to {DEFAULT_NUM_THREADS}"
    )

    args = parser.parse_args()

    if (args.attack == 'http' or args.attack == 'https'):
        args.method = input('Choice an HTTP method [GET, POST] : ').upper()

    return args
