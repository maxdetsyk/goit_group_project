"""
1. Сохранять контакты с именами, адресами, номерами телефонов, email и днями рождения в книгу контактов.
"""

from collections import UserDict
import datetime
import pickle
import re
from typing import List


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
        self.value = new_value

    def __eq__(self, other: object) -> bool:
        return self.value == other.value


class Birthday:
    def __init__(self, value):
        self.__value = datetime.strptime(re.sub("[- //]", ".", value), "%d.%m.%Y")

    def __repr__(self):
        return f"{self.__value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Email:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


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
    def __init__(
        self,
        name: Name,
        phone: List[Phone],
        birthday: Birthday,
        email: Email,
        address: Address,
    ) -> None:
        self.name = name
        if phone is None:
            self.phone = []
        else:
            self.phone = phone
        self.birthday = birthday
        self.email = email
        self.address = address

    def add_phone(self, phone):
        if phone not in self.phone:
            self.phone.append(phone)

    def __repr__(self) -> str:
        return f"Name: {self.name.value}\
                Phones: {', '.join([str(phone.value) for phone in self.phones])}\
                Birthday: {self.birthday}\
                Email:{self.email}\
                Address: {self.address}"


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
                self.curr_index : min(
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

    def delete_record(self, value: Name):
        self.data.pop(value.value)

    def __str__(self) -> str:
        return str(self.data)

    def iterator(self, count_records) -> AddressBookIterator:
        return AddressBookIterator(self.data, count_records)

    def save(self):
        with open("data.json", "bw") as file:
            pickle.dump(self.data, file)

    def load(self):
        try:
            with open("data.json", "br") as file:
                self.data = pickle.load(file)
        except:
            pass


CONTACT_BOOK = AddressBook()

"""
2. Выводить список контактов у которых день рождения через заданное количество дней от текущей даты.
"""


"""
3. Проверять правильность введенного номера телефона и email во время создания или редактирования записи и уведомлять пользователя в случае некорректного ввода.
"""


"""
4. Совершать поиск по контактам из книги контактов.
"""


class Asisstant:
    def __init__(self):
        self.address_book = AddressBook()

    def find_contact(self, name):
        result = self.address_book.find_record(name)
        print(result)


"""
5. Редактировать и удалять записи из книги контактов.
"""
