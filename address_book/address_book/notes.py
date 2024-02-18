from collections import UserDict


class Item:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __str__(self):
        return f"{self.title} {self.text}"


class Notes(UserDict):

    def add_note(self, title, text):
        idx = len(self.data)+1 if len(self.data) > 0 else 1
        self.data[idx] = Item(title, text)

        return self.get_notes()
    
    def get_notes(self):
        notes = '{:<30}| {:<80}\n'.format("Title", "Text")
        for note in self.data.values():
            notes += '{:<30}| {:<80}\n'.format(note.title, note.text)
        return notes

    def find_notes(self, text_to_find):
        text_to_find = text_to_find
        notes_found = Notes()
        for note in self.data.values():
            if note.title.lower().find(text_to_find.lower()) != -1\
                or note.text.lower().find(text_to_find.lower()) != -1:
                notes_found.add_note(note.title, note.text)
        
        return notes_found
