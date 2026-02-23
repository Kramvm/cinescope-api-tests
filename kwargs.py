def greet(**kwargs):
    print(kwargs)

greet(name="belis", idol = "pharaoh")

def create_dict(**kwargs):
    return kwargs
print(create_dict(a=1, b=2, c=3))
# Вывод: {'a': 1, 'b': 2, 'c': 3}

def update_settings(**kwargs):
    default_settings = {"theme": "light", "notifications": True}
    default_settings.update(kwargs)
    print(default_settings)
    return default_settings

print(update_settings(theme="dark", volume=80))
# Вывод: {'theme': 'dark', 'notifications': True, 'volume': 80}

def filter_kwargs(**kwargs):
    b = {}
    for key, value in kwargs.items():
        if value > 10:
            b[key] = value
    return b

print(filter_kwargs(a=5, b=20, c=15, d=3))
# Вывод: {'b': 20, 'c': 15}


def log_kwargs(func):
    def wrapper(*args, **kwargs):  # ← Принимает все аргументы оригинальной функции
        # 1. Выводим kwargs
        print(f"Called with kwargs: {kwargs}")  # ← Только kwargs!
        # 2. Вызываем оригинальную функцию
        return func(*args, **kwargs)
    return wrapper

@log_kwargs
def my_function(a, b, **kwargs):
    return a + b

my_function(5, 10, debug=True, verbose=False)
# Вывод:
# Called with kwargs: {'debug': True, 'verbose': False}

def add_numbers(*args):
    print(sum(args))

add_numbers(55,66,1000)

def create_list(*args):
    return list(args)

print(create_list(1, "apple", True, 3.14))  # [1, "apple", True, 3.14]


def pass_arguments(*args):
    print_args(*args)


def print_args(*args):
    for arg in args:
        print(arg)

pass_arguments("Hello", 42, False)
# Вывод:
# Hello
# 42
# False

def find_max(*args):
    return max(*args)

print(find_max(10, 20, 5, 100, 50))  # 100

def join_strings(*args):
    b = ''
    for a in args:
        b += f"{a} "
    return b

print(join_strings("Hello", "world", "!"))  # "Hello world !"

def process_data(*args, **kwargs):
    print(args)
    print(kwargs)

process_data(1, 2, 3, name="Alice", age=25)
# Вывод:
# Positional arguments: (1, 2, 3)
# Keyword arguments: {'name': 'Alice', 'age': 25}

def configure_function(*args, **kwargs):
    config = {}
    for key in args:
        if key in kwargs:
            config[key] = kwargs[key]
    return config

print(configure_function("theme", "volume", theme="dark", volume=50))
# Вывод: {'theme': 'dark', 'volume': 50}

def log_args_kwargs(func):
    def wrapp(*args, **kwargs):
        print(f"Positional arguments: {args}")
        print(f"Keyword arguments: {kwargs}")
        return func(*args, **kwargs)
    return wrapp


@log_args_kwargs
def my_function(x, y, **kwargs):
    return x + y

my_function(10, 20, debug=True, verbose=False)
# Вывод:
# Positional arguments: (10, 20)
# Keyword arguments: {'debug': True, 'verbose': False}