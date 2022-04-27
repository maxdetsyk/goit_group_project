CONTACT_BOOK = AddressBook()

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

def add_contact(args):
    name = args[0]

    if len(args) == 1:
        phone_book.add_record(Record(Name(name), None, None, None, None))
        print(f"The record with {name} was added")
    elif phone_book.find_record(Name(name)):
        result = phone_book.find_record(Name(name))
        result.add_phone(Phone(args[1]))
        print(f"The phone was added for the {name}.")
    elif len(args) == 2:
        phone_book.add_record(Record(Name(name), Birthday(args[1]), None, None,None))
        print(f"The record with {name} and biethday was added")
    elif len(args) == 3:
        phone_book.add_record(
            Record(Name(name), Birthday(args[1]), Email(args[2]), None, None))
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
    phone_book.load_data()

    while True:
        c = input("Enter a command: ")
        args = c.strip().split(" ")

        if args[0].lower() == "add":
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
        else:
            print("This command is unlnown. Try again!")

    phone_book.save_data()  
