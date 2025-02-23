from src import show_banner
from src.arg_parser import ArgParser
from src import TargetValidator
from src.config import Config
from src.dos import Dos, TCP, UDP


def main():
    trying_connection()


def trying_connection():
    parser = ArgParser()
    args = parser.parse_args()
    Config().init(args)

    target = args.target
    target_port = args.port
    attack_type = args.attack

    target_validator = TargetValidator(target)
    target_validated = target_validator.validate()

    if target_validated:
        print('Continue')

        attack(target, target_port, attack_type)
    else:
        print('End !')


def attack(target, target_port, attack_type):
    """
    target
    target_port
    attack_type: attack method like: UDP, HTTP
    """
    if attack_type == 'udp':
        dos_attacks = Dos(target, target_port, UDP, thread_number=6)
        return dos_attacks.start_attack()
    elif attack_type == 'http':
        print('HTTP')


if __name__ == "__main__":
    show_banner()
    main()
