from collections import UserDict


class Item:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"{self.text}"


class Notes(UserDict):

    def add_note(self, text):
        idx = len(self.data)+1 if len(self.data) > 0 else 1
        self.data[idx] = Item(text)
        return self.data

    def __str__(self):
        notes = '{:<5} | {:<50}\n'.format("ID", "Text")
        for key, value in self.data.items():
            notes += '{:<5} | {:<50}\n'.format(key, str(value))
        return notes

