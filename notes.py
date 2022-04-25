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
      
      
      
'''
7. Проводить поиск по заметкам.
'''
def find_note(self, subtext: str) -> list:
    """Method to find notes by text or ID"""
    subtext = subtext.lower()
    notes_list = []
    for note in self.data:

        if subtext in note.text.lower() or subtext == str(note.number):
            notes_list.append(note)
    return list(set(notes_list)) if notes_list else [f'{subtext} not found in notes.']


"""
8. Редактировать и удалять заметки
"""
    def del_note(self, number_arg: str):
        """Method to delete note by number"""
        try:
            number_arg = int(number_arg)
        except ValueError:
            print(f"Wrong input must be an integer")
        del_note_flag = None 
        for note in self.data:
            for key in note.note_dict.keys():
                if number_arg == note.note_dict(key):
                    del_note_flag = note
        if del_note_flag:
            self.data.remove(note)
        else:
            print('No note with this number')
            

    def change_note(self, number_arg: str, new_note: str):
        """Method searches for a note by number and changes its text"""
        try:
            number_arg = int(number_arg)
        except ValueError:
            print("Wrong input must be an integer")
        for note in self.data:
            for key in note.note_dict.keys():
                if number_arg == note.note_dict(key):
                    del_note_flag = note
        if del_note_flag:
            self.data.remove(note)
            self.data.append({RecordNote(NoteID(number_arg),Note(new_note))}) 
        else:
            print("No note with this number if u wanna add print another command")



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



