from collections import UserDict
from datetime import date, datetime
import os
import pickle
import re


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
    def __intit__(self, value) -> None:
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.value = new_value


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
    def value(self, new_value):
        if Phone.check_phone(new_value):
            self.__value = clear_phone(new_value)
        else:
            print("Phone have wrong format. Try again!")

    def __eq__(self, other: object) -> bool:
        return self.value == other.value

    @staticmethod
    def check_phone(phone):
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
    def value(self, new_value):
        if Birthday.__check_date(new_value):
            self.__value = new_value
        else:
            print("Date have wrong format. Try again!")

    @staticmethod
    def __check_date(date):
        date_form = re.sub("[- //]", ".", date)
        try:
            data = datetime.strptime(date_form, "%d.%m.%Y")
            return str(data)
        except ValueError:
            return None


class Email:
    def __init__(self, value):
        Email.check_email(value)
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if Email.check_email(new_value):
            self.__value = new_value
        else:
            print("Email have wrong format. Try again!")

    @staticmethod
    def check_email(email):
        result = re.match(r"[a-zA-Z]\.?\S+@\w{1,6}\.[\w]{1,4}", email)
        return result

    def __eq__(self, other: object) -> bool:
        return self.value == other.value


class Address:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Record:

    def __init__(self,
                 name: Name,
                 birthday: Birthday,
                 email: Email,
                 address: Address,
                 *args) -> None:

        self.name = name
        self.phones = []
        self.birthday = ''
        self.email = ''
        self.address = ''
        for item in args:
            if isinstance(item, Phone):
                self.phones.append(item)
        if isinstance(birthday, Birthday):
            self.birthday = birthday
        if isinstance(email, Email):
            self.email = email
        if isinstance(address, Address):
            self.address = address

    def add_phone(self, phone_number: str) -> list:
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    # changing phone in record with 2 string arguments in method

    def change_phone(self, phone_arg: str, replace_phone_arg: str):
        count = 0
        for i in range(len(self.phones)):
            if phone_arg == self.phones[i].value:
                self.phones[i] = Phone(replace_phone_arg)
                count += 1
        if count == 0:
            print(f'No such phone {phone_arg} in a record')

    def delete_phone(self, phone):

        for item in self.phone:
            if phone.value == item.value:
                new_phones_list = self.phones.remove(item)
                return new_phones_list

        print(f'No such phone number {phone} in record {self.name}')

    def add_email(self, email):
        if email not in self.email:
            self.email = email

    def edit_birthday(self, new_birthday):
        self.birthday.value = new_birthday

    def edit_email(self, new_email):
        self.email.value = new_email

    def edit_address(self, new_address):
        self.address.value = new_address

    def __repr__(self) -> str:
        return f"Name: {self.name.value}\
                Phones: {', '.join([str(phone.value) for phone in self.phones])}\
                Birthday: {self.birthday}\
                Email:{self.email}\
                Address: {self.address}"

    def days_to_birthday(self):
        """
        If birthday is added: counts days before next one.
        """

        if self.birthday.value is None:
            print(f"No b-day added for {self.name.value}")
            return

        date_now = date.today()
        birthday_date = self.birthday.value
        birthday_date = birthday_date.replace(year=date_now.year)
        # Check if user's birthday passed this year => year + 1
        if birthday_date <= date_now:
            birthday_date = birthday_date.replace(year=date_now.year + 1)

        days_delta = birthday_date - date_now
        return days_delta.days

    def birthday_in_next_x_days(self, step: int = 7):
        try:
            step = int(step)
        except ValueError:
            raise ValueError("Input a number")
        result = []
        for record in self.data.values():
            if record.birthday and record.birthday.value:
                if record.days_to_birthday() <= step:
                    birthday = f'{record.name.value} {record.birthday.value.strftime("%d-%m-%Y")}'
                    result.append(birthday)
        return result


class AddressBookIterator:
    def __init__(self, data, count_records) -> None:
        self.data = data
        self.curr_index = 0
        self.number_of_records = count_records

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_index < len(self.data):
            to_show = list(self.data.items())[
                self.curr_index: min(
                    len(self.data), self.curr_index + self.number_of_records
                )
            ]
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

    '''def delete_record(self, value: Name):
        self.data.pop(value.value)'''
    # AddressBook object method gets as an argument Record object

    def delete_record(self, obj):
        if isinstance(obj, Record):
            del self.data[obj.name.value]
            return self.data

    def __str__(self) -> str:
        return str(self.data)

    def iterator(self, count_records) -> AddressBookIterator:
        return AddressBookIterator(self.data, count_records)

    def save_contacts(self) -> None:
        folder_sep = "\\"

        fellow_folder = os.environ["HOMEPATH"] + folder_sep + "fellow"

        if os.path.exists(fellow_folder):
            with open(fellow_folder + folder_sep + "contacts.bin", "wb") as file:
                pickle.dump(self.data, file)
        else:
            os.mkdir(fellow_folder)
            with open(fellow_folder + folder_sep + "contacts.bin", "wb") as file:
                pickle.dump(self.data, file)

    def load_contacts(self) -> None:

        folder_sep = "\\"

        fellow_notes = (
            os.environ["HOMEPATH"] + folder_sep +
            "fellow" + folder_sep + "contacts.bin"
        )

        if os.path.exists(fellow_notes):
            with open(fellow_notes, "rb") as file:
                self.data = pickle.load(file)


CONTACT_BOOK = AddressBook()