from collections import UserDict
from datetime import date, datetime, timedelta
import pickle
from struct import unpack
import sys
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


    def find_contact(self, name):
        result = self.address_book.find_record(name)
        print(result)

"""
Sorting
"""
class Sorting:
    def __init__(self, path):
        self.path = path

folders_dict = {'images': ('.JPEG', '.PNG', '.JPG', '.SVG'),
          'documents': ('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX'),
          'video': ('.AVI', '.MP4', '.MOV', '.MKV'),
          'audio': ('.MP3', '.OGG', '.WAV', '.AMR'),
          'archives': ('.ZIP', '.GZ', '.TAR')}

LATIN_SYMBOLS = 'abvhgdezyijklmnoprstuf\'ABVHGDEZYIJKLMNOPRSTUF\''
CYRILLIC_SYMBOLS = 'абвгґдезиійклмнопрстуфьАБВГҐДЕЗИІЙКЛМНОПРСТУФЬ'
TRANS = {}


for l, s in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):
    TRANS[ord(l)] = s


def normalize_names(file_name):
    for sym in file_name:
        if sym not in LATIN_SYMBOLS and sym != int:
            sym.replace(sym, "_")
    return file_name.translate(TRANS)


def create_folders(path):
    for keys in folders_dict.keys():
        if not os.path.exists(os.path.join(path, keys)):
            os.mkdir(os.path.join(path, keys))


def sort_files(file_list, path):
    for file in file_list:
        if not os.path.isfile(os.path.join(path, file)):
            continue
        know = False
        file_name, file_ext = os.path.splitext(file)
        for key, value in folders_dict.items():
            if file_ext.upper() in value:
                src = os.path.join(path, normalize_names(file_name)+file_ext)
                dst = os.path.join(path, key, file_name+file_ext)
                os.replace(src, dst)
                know = True
            continue
        if not know:
            print(f'Unknown: {file_name}')



def make_list_files(path):
    os.listdir(path)
    create_folders(path)
    sort_files(os.listdir(path), path)


try:
    ps_2 = sys.argv[1]
    make_list_files(ps_2)
except IndexError as e:
    print(e)
