import argparse


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

    args = parser.parse_args()

    if (args.attack == 'http' or args.attack == 'https') and not args.method:
        parser.error(
            'The option --method (-m) is required with http(s) attacks')

    return args
