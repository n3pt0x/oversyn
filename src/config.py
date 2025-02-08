class Config():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.verbose = False
        return cls._instance

    @classmethod
    def init(cls, args):
        instance = cls()
        instance.verbose = args.verbose

    @classmethod
    def get_verbose(cls):
        return cls().verbose
