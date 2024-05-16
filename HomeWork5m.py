'''
1
'''

def caching_fibonacci():
    cache = {}  # поясніть як тут впливає словник? що він зберігає?
    def fibonacci(n):  # звичайний фібоначі
        if n <= 0: 
            return 0
        elif n == 1:
            return 1
        elif n in cache:
            return cache[n]  # чому тут цей словник який нічого не зберігає?
        
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]   # дежавю
    return fibonacci


'''
2
'''

from typing import Callable
import re

text = '''Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений 
    додатковими надходженнями 27.45 і 324.00 доларів.'''

def generator_numbers(text: str):
    numbers = re.findall(r"\d+\.\d+", text) # відділяю текст від цифр по формату цифри точка цифри
    for number in numbers:  
        yield float(number)   # через генератор назначаю перебирання цифр що отримав з тексту

def sum_profit(text: str, func: Callable[[float], float]) -> None: # отримую флоат оскільки мій генератор вже дає флоат
    gen = func(text)    # назначаю аргумент генератору щоб його перебрати
    total_salary = 0    # назначаю перемінну з загальною суммою що мені генератор нагенерує))
    for salary in gen:    #  грубо кажучи запускаю свій генератор з попередньої функції щоб всі числа перепрацював
        total_salary += salary    # суммую їх в свою перемінну
    return total_salary   # ну і вже звичайним поверненням виведу сумму яку нагенерував собі

total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")

'''
3
'''

# на доопрацюванні

'''
4
'''

import sys


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
    return inner

def change_errore(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command."
    return inner

def show_phone_errore(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Enter the argument for the command."
    return inner
        


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@change_errore
def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact changed."
    else:
        return "This name was not found in contacts."


@show_phone_errore
def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return f"{name}'s phone number is: {contacts[name]}"
    else:
        return "This name was not found in contacts."
    
def main():
    contacts = {}
    print("Welcome to the assistant bot! Click the 'help' button to learn about all the commands.")
    while True:
        print("help/close/exit/add/change/phone/all")
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            sys.exit(1)
        elif command == "hello":
            print("How can I help you? Please enter 'add' your name and number.")
        elif command == "help":
            print("You can:")
            print("add - add name and phone number;")
            print("close\exit - if you want quit;")
            print("change - if you need to do some change;")
            print("phone - you need enter name to see phone number")
            print("all - to see all list that you add")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(f"Here's all contacts that you've added: {contacts}. Do you need to make any changes?")
        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()
