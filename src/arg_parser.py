import argparse
from src.config import DEFAULT_NUM_THREADS
from src.utils import color_text

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
        "--http-method",
        type=str,
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
        "--threads",
        type=int,
        default=None,
        help=f"Number of threads, default set to {DEFAULT_NUM_THREADS}"
    )

    parser.add_argument(
        "--monothread",
        type=int,
        default=None,
        help="Use a mono thread, usefull for local test"
    )

    args = parser.parse_args()

    if args.attack in ('http', 'https'):
        while True:
            if (method := input('Choose an HTTP method [GET, POST]: ').strip().upper()) in ('GET', 'POST'):
                args.http_method = method
                break
            color_text('red', '[!] Only these methods are available [GET, POST]')
    return args
