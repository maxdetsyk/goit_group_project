from collections import UserDict
from datetime import date, datetime, timedelta
import pickle
import re
from typing import List

"""
1. Сохранять контакты с именами, адресами, номерами телефонов, email и днями рождения в книгу контактов.
"""


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


"""
3. Проверять правильность введенного номера телефона и email во время создания или редактирования записи и уведомлять пользователя в случае некорректного ввода.
"""
class Field:
   
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

class Phone(Field):
   
    def __init__(self, value):
        if re.fullmatch("\+\\d{12}", value):
            super().__init__(value)# self.value = value
        else:
            print(f"Wrong format for phone: {value}, please enter in format +380987654321")
            self.value = []

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other)-> bool:
        return self.value == other.value
    
class Email(Field):
    def __init__(self, value):
        if value is not None:
            if (re.match(r"[a-zA-Z]\.?\S+@\w{1,6}\.[\w]{1,4}", value)is not None):
                super().__init__(value)# self.value = value
            else:
                print(f'Wrong format for email: {value}')
                self.value = None
        else:
            self.value = None

def add_phone(self, new_phone: Phone):
    phone = Phone(new_phone)
    if phone not in self.phones:
        self.phones.append(phone)
        print("Phone add successfully.")
    return self.phones

def del_phone(self, new_phone: Phone):
    if new_phone in self.phones:
        self.phones.remove(new_phone)
    else:
        print("This phone not in base")
    return self.phones

def change_phone(self, old_phone: Phone, new_phone: Phone):
    new_phone = Phone(new_phone)
    if old_phone in self.phones:
        for x, result in enumerate(self.phones):
            if result == old_phone:
                self.phones[x] = new_phone
                print("Phone change successfully.")
    else:
        print("This phone not in base")
    return self.phones

def add_email(self, email):
    if email not in self.email:
        self.email = Email(email)
       

#d=Phone("+38093444557v")
#print(d.value)
#m=Email("vovsan555@i.ua")
#print(m.value)


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
