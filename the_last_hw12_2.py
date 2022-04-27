from datetime import datetime
from typing import List
from collections import UserDict
import re
import pickle


def clear_phone(phone):
    return (
        phone.strip()
        .removeprefix("+38")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )


class Field:
    def __init__(self, value) -> None:
        self.__value = value
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if Phone.__check_phone(value):
            self.__value = clear_phone(value)
        else:
            raise ValueError

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    @staticmethod
    def __check_phone(phone):
        new_phone = clear_phone(phone)
        if len(new_phone) == 10 and new_phone.isdigit():
            return True
        else:
            return False


class Birthday:
    def __init__(self, value):
        Birthday.__check_date(value)
        self.__value = datetime.strptime(
            re.sub("[- //]", ".", value), "%d.%m.%Y")

    def __repr__(self):
        return f"{self.__value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if Birthday.__check_date(value):
            self.__value = value
        else:
            raise ValueError

    @staticmethod
    def __check_date(date):
        date_form = re.sub("[- //]", ".", date)
        try:
            data = datetime.strptime(date_form, "%d.%m.%Y")
            return str(data)
        except ValueError:
            return None


class Record:
    def __init__(self, name: Name, phones: List[Phone], birthday: Birthday) -> None:
        self.name = name
        if phones is None:
            self.phones = []
        else:
            self.phones = phones
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone not in self.phones:
            self.phones.append(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        for phone in self.phones:
            if phone.value == old_phone.value:
                phone.value = new_phone.value

    def delete_phone(self, phone_number: Phone):
        for phone in self.phones:
            if phone.value == phone_number.value:
                self.phones.remove(phone)

    def days_to_birthday(self):
        if self.birthday:
            current_day = datetime.today()
            currrent_bd_year = self.birthday.value.replace(
                year=current_day.year)

            if current_day > currrent_bd_year:
                currrent_bd_year = currrent_bd_year.replace(
                    year=current_day.year+1)

            days_left = (currrent_bd_year - current_day).days

            print(f"{days_left} days to next birthday this contact.")
            return days_left
        else:
            print("Sorry we don't know your birthday")

    def __repr__(self) -> str:
        return f"Name: {self.name.value},\
                 Phones: {', '.join([str(phone.value) for phone in self.phones])} \
                 Birthday: {self.birthday}"


class AddressBookIterator:
    def __init__(self, data, count_records) -> None:
        self.data = data
        self.curr_index = 0
        self.number_of_records = count_records

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_index < len(self.data):
            to_show = list(self.data.items())[self.curr_index:min(
                len(self.data), self.curr_index + self.number_of_records)]
            self.curr_index += self.number_of_records
            return to_show
        else:
            raise StopIteration


class AddressBook(UserDict):
    def __init__(self):
        UserDict.__init__(self)

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec

    def find_record(self, name: Name) -> Record:
        return self.data.get(name.value)

    def delete_record(self, value: Name):
        self.data.pop(value.value)

    def __str__(self) -> str:
        return str(self.data)

    def iterator(self, count_records) -> AddressBookIterator:
        return AddressBookIterator(self.data, count_records)

    def save(self):
        with open('data.json', 'bw') as file:
            pickle.dump(self.data, file)

    def load(self):
        try:
            with open('data.json', 'br') as file:
                self.data = pickle.load(file)
        except:
            pass


def input_error(function):
    def inner(args):
        try:
            return function(args)
        except KeyError:
            print("Not such name exist.")
        except ValueError:
            print("Enter the name and number after the command separated by a space.")
        except IndexError:
            print("Phone book is empty.")
    return inner


def greeting_command():
    print("How can I help you?")


@input_error
def add_contact(args):
    name = args[0]

    if len(args) == 1:
        phone_book.add_record(Record(Name(name), [], None))
        print(f"The record with {name} was added without phone")
    elif phone_book.find_record(Name(name)):
        result = phone_book.find_record(Name(name))
        result.add_phone(Phone(args[1]))
        print(f"The phone was added for the {name}.")
    elif len(args) == 2:
        phone_book.add_record(Record(Name(name), [Phone(args[1])], None))
        print("Contact added successfully")
    else:
        phone_book.add_record(
            Record(Name(name), [Phone(args[1])], Birthday(args[2])))
        print(f"The contact {name} was added with phone number and birthday ")


@input_error
def change_phone_number(args):
    name, old_phone, new_phone = args
    if phone_book.find_record(Name(name)):
        result = phone_book.find_record(Name(name))
        result.edit_phone(Phone(old_phone), Phone(new_phone))
        print(f"Phone number for the {name} was changed successfuly.")
    else:
        print(
            f"Record for the {name} does not exist. Enter the correct name, please.")


@input_error
def get_phone_number(args):
    name = args[0]
    result = phone_book.find_record(Name(name))
    print(result)


@input_error
def delete_record(args):
    name = args[0]
    phone_book.delete_record(Name(name))
    print(f"The record with {name} was deleted successfuly")


@input_error
def remove_phone(args):
    name, phone = args
    result = phone_book.find_record(Name(name))
    result.delete_phone(Phone(phone))
    print(f"The phone for the {name} was removed successfuly.")


@input_error
def search_phone(args):
    keyword = args[0].lower().strip()

    for rec in phone_book.values():
        if keyword in rec.name.value.lower():
            print(rec)
            continue
        for phone in rec.phones:
            if keyword in phone.value:
                print(rec)
                break


@input_error
def show_all_contacts(args):
    number_of_entries = 1 if len(args) == 0 else int(args[0])
    if number_of_entries:
        for n in phone_book.iterator(number_of_entries):
            print(n)
    else:
        print("Specify the number of records to display line by line")


@input_error
def next_birthday(args):
    name = args[0]
    result = phone_book.find_record(Name(name))
    result.days_to_birthday()


def exit_command():
    print("Good bye!")


phone_book = AddressBook()


def main():
    phone_book.load()

    while True:
        c = input("Enter a command: ")
        args = c.strip().split(" ")

        if args[0].lower() == "hello":
            greeting_command()
        elif args[0].lower() == "add":
            add_contact(args[1:])
        elif args[0].lower() == "phone":
            get_phone_number(args[1:])
        elif args[0].lower() == "change":
            change_phone_number(args[1:])
        elif args[0].lower() == "delete":
            delete_record(args[1:])
        elif args[0].lower() == "remove":
            remove_phone(args[1:])
        elif args[0].lower() == "search":
            search_phone(args[1:])
        elif args[0].lower() == "birthday":
            next_birthday(args[1:])
        elif len(args) >= 2 and f"{args[0]} {args[1]}".lower() == "show all":
            show_all_contacts(args[2:])
        elif len(args) >= 2 and f"{args[0]} {args[1]}".lower() == "good bye" \
                or args[0].lower() == "close" or args[0].lower() == "exit":
            exit_command()
            break
        else:
            print("This command is unlnown. Try again!")

    phone_book.save()


if __name__ == "__main__":
    main()