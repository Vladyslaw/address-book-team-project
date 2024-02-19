from collections import UserDict, defaultdict


class Item:
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __str__(self):
        return f"{self.title} {self.text}"

class Tag:
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, tag):
        if type(tag) != Tag:
            return False
        
        return self.name == tag.name

class Tags:
    def __init__(self):
        self.tags = UserDict()
    
    def add_tag(self, name):
        new_tag = Tag(name)
        if new_tag in self.tags.data.values():
            return f'Tag with name {name} already exists!'
        
        index = len(self.tags) + 1 if len(self.tags) > 0 else 1
        self.tags[index] = new_tag
        return f'Tag with name {name} succesfully created!'
    
    def get_tags(self):
        tags = '{:<30}\n'.format('Tag')
        for tag_name in self.tags.data.values():
            tags += '{:<30}\n'.format(tag_name)
        return tags

class Notes(UserDict):

    def __init__(self):
        super().__init__()
        self.tags = defaultdict(list)

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
    
    def delete_note(self, title_text):
        for id, note in self.data.items():
            if title_text.lower().strip() in note.title.lower():
                del self.data[id]
                return "Removed note"
        return "No note with such title"
    

    def edit_note(self, title_text, new_text):
        for id, note in self.data.items():
            if title_text.lower().strip() in note.title.lower() or title_text.lower().strip() in note.title.lower():
                self.data[id] = Item(note.title, new_text)
                return self.get_notes()
        return "No note with such text"


    def add_tag(self, note_title=None, note_text=None):
        pass


if __name__ == '__main__':
    tags = Tags()
    print(tags.add_tag('tag1'))
    print(tags.add_tag('tag2'))
    print(tags.get_tags())