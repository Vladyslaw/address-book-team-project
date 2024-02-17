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

        notes = '{:<5}| {:<30}| {:<80}\n'.format("ID", "Title", "Text")
        for key, value in self.data.items():
            notes += '{:<5}| {:<30}| {:<80}\n'.format(key, value.title, value.text)
        return notes
