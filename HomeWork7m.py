from datetime import datetime
from HomeWork6m import *

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
        Phone

