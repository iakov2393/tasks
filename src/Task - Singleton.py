class SingletonMeta(type):
    """Синглтон через метакласс"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def __init__(self, value):
        self.value = value





class SingletonNew:
    """Синглтон через переопределение __new__"""
    _instances = None

    def __new__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instances = super().__new__(cls)
        return cls._instances

    def __init__(self, value):
        if not hasattr(self, "value"):
            self.value = value





class SingletonModule:
    """Синглтон через механизм ипортов"""
    def __init__(self, value):
        self.value = value