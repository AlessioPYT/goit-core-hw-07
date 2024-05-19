from collections import UserDict
from datetime import datetime, date, timedelta
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
    return start_date + timedelta(days=days_ahead)


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
        try:
            datetime.strptime(value, "%Y.%m.%d").date()
            if value == True:
                self.value = value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record():
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday.value
        

    def add_birthday(self):
        return self.phones.append(self.birthday)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)

class Phone(Field):
    def __init__(self, phone):
        if not self.valid_phone(phone):
             raise ValueError('Number must be 10 characters!')
        super().__init__(phone)

    def valid_phone(self, phone):
        if isinstance(phone, str) and phone.isdigit(): 
            return len(phone) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            return f"Name is already in list!"

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found in the address book.")
        

    def get_upcoming_birthdays(self, users, days=7):
        today = date.today()
        self.data = []

        for user in users:
            birthday_this_year = user["birthday"].replace(year=today.year)
            birthday_this_year = adjust_for_weekend(birthday_this_year)
            if birthday_this_year < today:
                birthday_this_year = adjust_for_weekend(user["birthday"].replace(year=today.year + 1))
            if 0 <= (birthday_this_year - today).days <= days:
                congratulation_date_str = date_to_string(birthday_this_year)
                self.data.append({"name": user["name"], "congratulation_date": congratulation_date_str})
        return self.data
    
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y.%m.%d").date()
            if value == True:
                self.value = value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record():
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday.value
        

    def add_birthday(self):
        return self.phones.append(self.birthday)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
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
    if not user_input.strip():
        return None, []
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
    record = book.find(name)  # знаходимо запис
    if record:
        record.phones = [Phone(phone)]  # додаємо новий телефон після його валідації
        return "Contact phone updated."
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
            print("close/exit - if you want quit;")
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
