import sys
from HomeWork6m import *
from HomeWork7m import *


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
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."
    

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record.birthday if record.birthday else "Birthday not set."

@input_error
def birthdays(args, book: AddressBook):
    if args in book:
        return AddressBook.get_upcoming_birthdays
    else:
        return "Theare is non one to be be congratulation"


@change_errore
def change_contact(args, book: AddressBook):
    name, phone = args
    if name in book:
        book[name] = phone
        return "Contact changed."
    else:
        return "This name was not found in contacts."


@show_phone_errore
def show_phone(args, book: AddressBook):
    name = args[0]
    if name in book:
        return f"{name}'s phone number is: {book[name]}"
    else:
        return "This name was not found in contacts."
    
def main():
    book = AddressBook()
    print("Welcome to the assistant bot! Click the 'help' button to learn about all the commands.")
    while True:
        print("help/close/exit/add/change/phone/all/add-birthday/show-birthday/birthdays")
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
            print("add-birthday - Add the date of birth for the specified contact.")
            print("show-birthday - Show the date of birth for the specified contact.")
            print("birthdays - Показати дні народження, які відбудуться протягом наступного тижня.")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(f"Here's all contacts that you've added: {book}. Do you need to make any changes?")
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()
