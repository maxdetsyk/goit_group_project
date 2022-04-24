"""
6. Сохранять заметки с текстовой информацией
"""
from collections import UserList
import pickle


class Note:

    def __init__(self, value) -> None:
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def note(self, new_note):
        self.__value = new_note



class NoteID:

    def __init__(self, value) -> None:
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_id):
        self.__value = new_id


class RecordNote:
    def __init__(self, number: NoteID, note: Note):
        self.number = number
        self.note = note
        self.note_dict = {self.number: self.note}

    def add_note(self, number, note):
        note_dict = {number: note}
        return note_dict


class NoteBook(UserList):
    def __init__(self):
        UserList.__init__(self)

    def add_record(self, recordNote: RecordNote):
        self.data[recordNote.number.value] = recordNote

    def save(self):
        with open('data.json', 'bw') as file:
            pickle.dump(self.data, file)

    def load(self):
        try:
            with open('data.json', 'br') as file:
                self.data = pickle.load(file)
        except:
            pass


"""
8. Редактировать и удалять заметки
"""
def del_note(self, number: int):
    """Method to delete note by number"""
    try:
        number = int(number)
    except ValueError as e:
        print(f"Wrong input: {e}, must be an integer")
    del_note = None
    for note in self.data:
        if number == note.number:
            del_note = self.data.pop(number)  # or pop(number-1)?
            print(f"Note number:{number} was deleted")
        else:
            print(f"Numder:{number} is not valide")


def change_note(self, number: str, new_note: str):
    """Method searches for a note by number and changes its text"""
    try:
        number = int(number)
    except ValueError as e:
        print(f"Wrong input: {e}, must be an integer")
    for note in self.data:
        if number == note.number:
            note.text = new_note
