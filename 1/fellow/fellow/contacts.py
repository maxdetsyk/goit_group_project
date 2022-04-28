from collections import UserDict
from datetime import datetime
import pickle
import re
from copy import copy

import os

class Field:
    
    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self) -> str:
        return self._value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self,value):
        self._value = value

    
class Name(Field):
    
    pass



class Phone(Field):
    
    @Field.value.setter
    def value(self, value):
        
        matched_phone = re.findall(r'^\+?\d+$',value)
        
        if (matched_phone and len(value) <= 15) or value == '':
            self._value = value           
        elif not matched_phone:
            print("Phone has to be no more then 15 digits and include or not '+' in the beginning")
            self._value = 'nothing'
        
        

            
class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        try:
            b_day = datetime.strptime(value, "%d/%m/%y").date()
            self._value = b_day

        except ValueError:
            print("Wrong birthday format, has to be dd/mm/yy ")



class Record:
    
    def __init__(self, name, *args):
        
        self.name = name
        self.phones = []
        self.birthday = ''       
        for item in args:
            if isinstance(item, Phone):
                self.phones.append(item)
            if isinstance(item, Birthday):
                self.birthday = item
                              
            
                
                
    def delete_phone(self, phone_arg):
        
        for item in self.phones:
            if phone_arg == item.value:
                a = self.phones.remove(item)                
                return a
            
        print(f'No such phone number {phone_arg} in record {self.name}')
                
    def add_phone(self, phone_arg):
        self.phones.append(Phone(phone_arg))
        
    def change_phone(self,phone_arg, replace_phone_arg):
        count = 0
        for i in range(len(self.phones)):
            if phone_arg == self.phones[i].value:
                self.phones[i] = Phone(replace_phone_arg)
                count += 1
        if count == 0:
            print(f'No such phone {phone_arg} in a record')
            
    def days_to_birthday(self):
        if not self.birthday:
            return 'No birthday in this record'
        
        
        today = datetime.today()
                
        if (today.month == self.birthday.value.month and today.day >= self.birthday.value.day or today.month > self.birthday.value.month):
            next_birthday_year = today.year +  1
        else:
            next_birthday_year = today.year
            
        next_birthday = datetime(next_birthday_year,self.birthday.value.month,self.birthday.value.day)
        difference = next_birthday - today
        return  difference.days        
                 
        #self.phones = [item if item.value != phone_arg else Phone(replace_phone_arg) for item in self.phones]
            
        
        

    def __str__(self):
        if isinstance(self.birthday,Birthday):
            birthday_str = self.birthday.value.strftime("%d/%m/%y")
            res = f"{self.name}  {', '.join([str(phone) for phone in self.phones])}, {birthday_str}"
        else:
            res = f"{self.name}  {', '.join([str(phone) for phone in self.phones])}"
            
        return res
    


class AddressBook(UserDict):

    printed_records = 0
    records_to_print = 0
    
    def add_record(self, obj):

        if isinstance(obj, Record):
            self.data[obj.name.value] = obj
            return True
        
    def delete_record(self,obj):
        if isinstance(obj, Record):
            del self.data[obj.name.value]
            
            return self.data
        
    def __next__(self):

        if len(self.data.items()) > self.printed_records:
            
            printed_chunk = list(self.data.items())[self.printed_records:self.printed_records + self.rows_to_print]
            printed_chunk_str  = "\n".join([str(value) for key,value in printed_chunk])
            self.printed_records = self.printed_records + self.rows_to_print

            return printed_chunk_str
        else:
            print("No more records to show")
            raise StopIteration
        
    def __iter__(self):
         return self

    def iterator_2(self, quantity):
        self.rows_to_print = quantity

        for record in self:
            print(record)
            return record   
        
    def iterator(self, rows_number=2):
        end = len(self.data)
        i = 0
        limit = rows_number
        while True:
            yield "\n".join([f"{str(item)}" for key,item in list(self.data.items())[i:limit]])
            print("next page")
            i, limit = i + rows_number, limit + rows_number
            if i >= end:
                break  

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value


    def search(self, text):
        #result = []
        for field in self.data.values():
            if text in field.name.value or [ph for ph in field.phones if text in ph.value]:
                print(f'{field}----serch result from----{text}')
        print('-----End of search------')        
                
        

    def __str__(self):
        return "\n".join([f"{str(v)}" for k, v in self.data.items()])



    def save_data(self) -> None:
        folder_sep = "\\"

        fellow_folder = os.environ["HOMEPATH"] + folder_sep + "fellow"

        if os.path.exists(fellow_folder):
            with open(fellow_folder + folder_sep + "contacts.bin", "wb") as file:
                pickle.dump(self.data, file)
        else:
            os.mkdir(fellow_folder)
            with open(fellow_folder + folder_sep + "contacts.bin", "wb") as file:
                pickle.dump(self.data, file)

    def load_data(self) -> None:

        folder_sep = "\\"

        fellow_notes = (
            os.environ["HOMEPATH"] + folder_sep +"fellow" + folder_sep + "contacts.bin"
        )

        if os.path.exists(fellow_notes):
            with open(fellow_notes, "rb") as file:
                self.data = pickle.load(file)

  


def show_contacts():
    a = str(adress_book)
    if len(a) == 0:
        print('The Adress Book is empty')
    else:
        print(adress_book)
    return True

def add_contact():
    operative_name = input('Enter name of contact:\n')
    
    while operative_name == '' or operative_name in adress_book.data.keys():
        print('Hey, this name exists or it\'s not good enough\n')
        operative_name = input('Enter name of contact:\n')
    rec = Record(Name(operative_name))   
    adress_book.add_record(rec)
    
    print('Now add phone number...')
    operative_phone = input()
    ph = Phone(operative_phone)       
    while ph.value == "nothing":
        print('Add one phone number its obligatory...')
        operative_phone = input()
        ph = Phone(operative_phone)
        if operative_phone == '':
            print('Okok, fellow, let it be only the the name for now...\n\n')
            break
    rec.add_phone(operative_phone)
    adress_book.save_data()
    print('Basic contact record created\nTo add or change stuff start from MENU all over again...\nYes i like to torture HAHAHA...;)')
    return True
    #adress_book.save_data()

def del_contact(arg):
    if arg in adress_book.data.keys():
        del adress_book.data[arg]
        print('Done!!! Out of the contact book!!!!...\n')
        adress_book.save_data()
    else:
        print('You did not tell me to remember this record before ...\nIknow U know what to do for adding;)\n')
        return False
        
def find_contact(arg):
    adress_book.search(arg)
    return True

adress_book = AddressBook()
adress_book.load_data()


