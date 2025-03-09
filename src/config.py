class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.verbose = False
            cls._instance.target = None
            cls._instance.port = None
            cls._instance.attack = None
            cls._instance.count = None
        return cls._instance

    def init(self, args):
        """Initialisation de la configuration avec les arguments."""
        self.verbose = args.verbose
        self.target = args.target
        self.port = args.port
        self.attack = args.attack
        self.count = args.count

    @staticmethod
    def get_verbose():
        """Accéder à la propriété 'verbose' sans instance."""
        return Config().verbose
