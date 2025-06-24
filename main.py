from src import show_banner
from src.arg_parser import arg_parser
from src import TargetValidator
from src.dos import HTTPDos, SocketDos, TCP, UDP, DEFAULT_NUM_THREADS
from src.utils import resume


def main():
    args = arg_parser()
    trying_connection(args)


def trying_connection(args):
    resume(args)

    target_validator = TargetValidator(args)
    target_validated = target_validator.validate()

    if target_validated:
        print('Packet sending ...')
        attack(args)
    else:
        print('End !')


def attack(args):
    """
    target
    target_port
    attack_type: attack method like: UDP, HTTP
    """
    if args.attack in ('udp', 'tcp'):
        return SocketDos(args).start_attack()
    elif args.attack in ('http', 'https'):
        return HTTPDos(args).start_attack()


if __name__ == "__main__":
    show_banner()
    main()
