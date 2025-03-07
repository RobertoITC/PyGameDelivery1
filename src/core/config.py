class Config:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.settings = {
                "WIDTH": 800,
                "HEIGHT": 600,
                "PLAYER_SPEED": 5,
                "BULLET_SPEED": 7
            }
        return cls._instance

    def get(self, key):
        return self.settings.get(key)