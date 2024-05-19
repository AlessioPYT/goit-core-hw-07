from collections import UserDict
from datetime import datetime, date, timedelta
from HomeWork3m import *

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

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
        
if __name__ == '__main__':
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
