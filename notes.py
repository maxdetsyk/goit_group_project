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
            del_note = self.data.pop(number)# or pop(number-1)?
            print(f"Note number:{number} was deleted")
        else:
            print(f"Numder:{number} is not valide")

def change_note(self, number: str, new_note: str):
    """Method searches for a note by number and changes its text"""
    try:
        number = int( number)
    except ValueError as e:
        print(f"Wrong input: {e}, must be an integer")
    for note in self.data:
        if number == note.number:
            note.text = new_note
