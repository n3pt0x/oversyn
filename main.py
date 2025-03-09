from src import show_banner
from src.arg_parser import ArgParser
from src import TargetValidator
from src.config import Config
from src.dos import Dos, TCP, UDP
from src.utils import *


def main():
    parser = ArgParser()
    args = parser.parse_args()

    config = Config()
    config.init(args)
    
    trying_connection()


def resume():
    config = Config()
    color_text(
        'yellow', f'target: {config.target}, port: {config.port}, attack: {config.attack}, packet number: {config.count if config.count else "Infinite"},\n')


def trying_connection():
    config = Config()
    target = config.target
    target_port = config.port
    attack_type = config.attack
    print(f'{config.port}')
    resume()

    target_validator = TargetValidator(target)
    target_validated = target_validator.validate()

    if target_validated:
        print('Packet sending ...')
        # attack(target, target_port, attack_type)
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
