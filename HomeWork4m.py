

'''
№ _1_
'''
    
def total_salary(path):    # py HomeWork4m.py
    salaries = []
    try:
        with open(path, 'r', encoding='utf-8', errors='strict') as file_path:
            for line in file_path:
                name, salary = line.strip().split(',')
                salaries.append(float(salary))
                total_salaries = sum(salaries)
                medium_salaries = total_salaries / len(salaries)
            tuple_salaries = (total_salaries, medium_salaries)
        return tuple_salaries
    except FileNotFoundError:
        print("This file not found, please check file path!")
    except UnboundLocalError:
        print("The information in the file does not match the submission format, please check!")
    except TypeError:
        print("Some error in file path, please chek it!")
        

total, average = total_salary("text.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")

'''
№ _2_
'''

def get_cats_info (path):
    general_info = []
    try:
        with open(path, 'r') as file_cats: 
            for line in file_cats:
                id_cat, name_cat, age_cat = line.strip().split(',')
                cats_info_dict = {'id': id_cat, 'name': name_cat, 'age': age_cat}
                general_info.append(cats_info_dict)
            return general_info
    except FileNotFoundError:
        print("This file not found, please check file path!")
    except UnboundLocalError:
        print("The information in the file does not match the submission format, please check!")
    except TypeError:
        print("Some error in file path, please chek it!")
    except ValueError:
        print("The information in the file does not match the submission format, please check!")
        

print(get_cats('text_cat.txt'))

'''
№ _3_
'''

import sys
from pathlib import Path
from colorama import init, Fore

init(autoreset=True)            # py train.py

def visualize_directory_structure(directory_path):
    directory = Path(directory_path)
    if not directory.is_dir():
        print(f"{Fore.RED}Error: The path is not a directory.")
        return
    for item in directory.iterdir():
        if item.is_dir():
            print(Fore.BLUE + "📁 " + item.name)
            visualize_directory_structure(item)
        else:
            print(Fore.GREEN + "📄 " + item.name)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Error: Please specify a directory path as a command line argument.")
        sys.exit(1)

directory_path = sys.argv[1] 
visualize_directory_structure(directory_path)

'''
№ _4_
'''

import sys

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):
    if len(args) != 2:
        return "Invalid input. Please provide name and phone number."
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    if len(args) != 2:
        return "Invalid input. Please provide name and phone number."
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact changed."
    else:
        return "This name was not found in contacts."

def show_phone(args, contacts):
    if len(args) != 1:
        return "Invalid input. Please provide name."
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


