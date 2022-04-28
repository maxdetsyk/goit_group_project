from collections import UserDict
import os
import pickle


class Topic:
    def __init__(self, topic):
        self.value = topic

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class Note:
    def __init__(self, note):
        self.note = note

    def __str__(self) -> str:
        return self.note

    def __repr__(self) -> str:
        return self.note    


class RecordNote:
    
    def __init__(self, topic, *args):
        self.topic = topic
        self.notes = []
        for item in args:
            if isinstance(item, Note):
                self.notes.append(item)

    def add_note(self, note_args) -> None:                           
        self.notes.append(Note(note_args))                     

    def __str__(self) -> str:
        return f"Topic: {self.topic}, Notes : {', '.join([str(p.note) for p in self.notes])}"

    def __repr__(self) -> str:
        return f"Topic: {self.topic}, Notes : {', '.join([str(p.note) for p in self.notes])}"


class NoteBook(UserDict):

    def save_data(self) -> None:
        folder_sep = "\\"

        fellow_folder = os.environ["HOMEPATH"] + folder_sep + "fellow"

        if os.path.exists(fellow_folder):
            with open(fellow_folder + folder_sep + "notes.bin", "wb") as file:
                pickle.dump(self.data, file)
        else:
            os.mkdir(fellow_folder)
            with open(fellow_folder + folder_sep + "notes.bin", "wb") as file:
                pickle.dump(self.data, file)

    def load_data(self) -> None:

        folder_sep = "\\"

        fellow_notes = (
            os.environ["HOMEPATH"] + folder_sep +
            "fellow" + folder_sep + "notes.bin"
        )

        if os.path.exists(fellow_notes):
            with open(fellow_notes, "rb") as file:
                self.data = pickle.load(file)


    def add_record(self, obj):
        
        if isinstance(obj, RecordNote):
            if obj.topic.value in self.data.keys():
                self.data.update({obj.topic.value: obj})
            else:
                self.data[obj.topic.value] = obj

    def edit_note(self, topic, new_note: Note) -> str:
        self.data[topic] = new_note


    def delete_whole_record(self, obj):
        if isinstance(obj, RecordNote):
            del self.data[obj.topic.value]

    def __str__(self) -> str:
        result = "\n".join([str(rec) for rec in self.data.values()])
        return result

note_book = NoteBook()

note_book.load_data()

def add_note():
    operativ_topic = input("Enter nesessary topic:\n")
    while operativ_topic == "":
        print("Brother, enter correct name! Because I will be angry!\n")
        operativ_topic = input()
    operativ_note = input("Enter your note:\n")
    while operativ_note == "":
        print("You are so boaring, write something smarter!\n")
        operativ_note = input()
    record_note = RecordNote(Topic(operativ_topic), Note(operativ_note))
    note_book.add_record(record_note)
    note_book.save_data()
    return True

def change_note():
    operativ_topic = input("Enter needed topic to change:\n")
    if operativ_topic not in note_book.data.keys():
        print("This topic does not exist!")
    else:
        new = input("Enter new note:\n")
        note_book.edit_note(operativ_topic, RecordNote(Topic(operativ_topic), Note(new)))
        note_book.save_data()
        print("Note was changed")

def delete_note(arg):
    if arg in note_book.data.keys():
        del note_book.data[arg]
        print(f'Done!!! Note of this topis {arg} was deleted !!!!...\n')
        note_book.save_data()
    else:
        print('You did not tell me about this topic before ...\n I know you know what to do for adding;)\n')
        return False

def show_notes():
    a = str(note_book)
    if len(a) == 0: 
        print('The Note book is empty')
    else:
        print(note_book)
    return True