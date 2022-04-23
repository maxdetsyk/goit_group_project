# goit_group_project

goit python group project - personal assistant

import re

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
        if len(value) == 13 and value[0] == "+" and value[1:].isdigit():
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
def **init**(self, value):
if value is not None:
if (re.match(r"[a-zA-Z]\.?\S+@\w{1,6}\.[\w]{1,4}", value)is not None):
super().**init**(value)# self.value = value
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
