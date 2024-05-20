from collections import UserDict
from datetime import datetime, date, timedelta
import re
import sys


def string_to_date(date_string):
    return datetime.strptime(date_string, "%Y.%m.%d").date()


def date_to_string(date):
    return date.strftime("%Y.%m.%d")


def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            self.value = datetime.strptime(value, "%Y.%m.%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY.MM.DD")


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone):
        if not self.valid_phone(phone):
            raise ValueError('Number must be 10 digits!')
        super().__init__(phone)

    def valid_phone(self, phone):
        return isinstance(phone, str) and re.match(r'^\d{10}$', phone)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if not phone:
            raise ValueError
        index = self.phones.index(phone)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = '; '.join(str(p) for p in self.phones)
        birthday = str(self.birthday) if self.birthday else "Not set"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            return "Name is already in the list!"

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found in the address book.")

    def get_upcoming_birthdays(self, days=7):
        today = date.today()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                if birthday_this_year.weekday() >= 5:
                    birthday_this_year = find_next_weekday(birthday_this_year, 0)
                if 0 <= (birthday_this_year - today).days <= days:
                    congratulation_date_str = date_to_string(birthday_this_year)
                    upcoming_birthdays.append({"name": record.name.value,
                                               "congratulation_date": congratulation_date_str})
        return upcoming_birthdays

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments provided."
    return inner


def change_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command."
    return inner


def show_phone_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Enter the argument for the command."
    return inner


def parse_input(user_input):
    if not user_input.strip():
        return None, []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Usage: add <name> <phone>"
    name, phone = args[:2]
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Usage: add-birthday <name> <birthday>"
    name, birthday = args[:2]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        return "Not enough arguments. Usage: show-birthday <name>"
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return str(record.birthday) if record.birthday else "Birthday not set."


@input_error
def birthdays(book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join(f"{entry['name']} - {entry['congratulation_date']}" for entry in upcoming_birthdays)
    else:
        return "There is no one to congratulate within the next week."


@change_error
def change_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Not enough arguments. Usage: change <name> <new_phone>"
    name, phone = args[:2]
    record = book.find(name)
    if record:
        record.phones = [Phone(phone)]
        return "Contact phone updated."
    else:
        return "This name was not found in contacts."


@show_phone_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        return "Not enough arguments. Usage: phone <name>"
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}'s phone number(s): {', '.join(str(p) for p in record.phones)}"
    else:
        return "This name was not found in contacts."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot! Click the 'help' button to learn about all the commands.")
    while True:
        print("help/close/exit/add/change/phone/all/add-birthday/show-birthday/birthdays")
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            sys.exit(1)
        elif command == "hello":
            print("How can I help you? Please enter 'add' your name and number.")
        elif command == "help":
            print("You can:")
            print("add - add name and phone number;")
            print("close/exit - if you want quit;")
            print("change - if you need to do some change;")
            print("phone - you need enter name to see phone number")
            print("all - to see all list that you add")
            print("add-birthday - Add the date of birth for the specified contact.")
            print("show-birthday - Show the date of birth for the specified contact.")
            print("birthdays - Show birthdays that will take place within the next week.")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(f"Here's all contacts that you've added:\n{book}. Do you need to make any changes?")
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
