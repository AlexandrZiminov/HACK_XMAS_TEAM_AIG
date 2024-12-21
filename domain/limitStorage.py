class LimitStorage:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LimitStorage, cls).__new__(cls)
            cls._instance._data = {}
        return cls._instance

    def set(self, key, value):
        self._data[key] = value

    def get(self, key):
        return self._data.get(key)

    def remove(self, key):
        self._data.pop(key, None)

    def items(self):
        return self._data.items()

    def update_limit_by_key(self, key, value):
        self._data[key] += value

    def get_limit_by_key(self, key):
        return self._data[key]
