from src import show_banner
from src.arg_parser import ArgParser
from src import TargetValidator
from src.config import Config

def main():
    trying_connection()


def trying_connection():
    parser = ArgParser()
    args = parser.parse_args()
    Config().init(args)

    target_validator = TargetValidator(args.target)
    target_validated = target_validator.validate()
    
    if target_validated:
        print('Continue')
    else:
        print('End !')


if __name__ == "__main__":
    show_banner()
    main()
