from typing import List
from typing import Optional
from typing import Union

def multiply(a : int, b : int) -> int:
    return a * b
print(multiply(16,"россия"))

def sum_numbers(numbers : List[int]) -> List[int]:
    return sum(numbers)
print(sum_numbers([11,122,33]))

def find_user(user_id : int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None
print(find_user(1))

def process_input(value : Union[int, str]) -> str:
    return f"Ты передал: {value}"
print(process_input("оу щет"))

class User:
    def __init__(self, name : str, age : int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"


user= User("Артем", 18)

print(user.greet())