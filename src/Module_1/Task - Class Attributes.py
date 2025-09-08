from datetime import datetime

class CreatedAtMeta(type):
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        cls.created_at = datetime.now()
        return cls


class MyClass(metaclass=CreatedAtMeta):
    pass


if __name__ == "__main__":
    print(MyClass.created_at)