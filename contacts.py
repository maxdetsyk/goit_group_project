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
        self.__value = datetime.strptime(
            re.sub("[- //]", ".", value), "%d.%m.%Y")

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

    def __init__(self,
                 name: Name,                 
                 birthday: Birthday,
                 email: Email,
                 address: Address,
                 *args) -> None:
        self.name = name
        self.phones =[]        
        self.birthday = ''
        self.email = ''
        self.address = ''
        for item in args:
            if isinstance(item, Phone):
                self.phones.append(item)
        if isinstance(birthday,Birthday):
            self.birthday = birthday
        if isinstance(email,Email):
            self.email = email
        if isinstance(address,Address):
            self.address = address    
        

    def add_phone(self, phone_number:str) -> list:
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)
            
    #changing phone in record with 2 string arguments in method
            
    def change_phone(self,phone_arg:str, replace_phone_arg:str):
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
            
        print(f'No such phone number {phone_arg} in record {self.name}')

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

    '''def delete_record(self, value: Name):
        self.data.pop(value.value)'''
    #AddressBook object method gets as an argument Record object
    def delete_record(self,obj):
        if isinstance(obj, Record):
            del self.data[obj.name.value]
            return self.data    

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



