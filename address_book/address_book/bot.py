import sys
import pickle
from classes import AddressBook, Record
from notes import Notes

commands_help = {
        'hello': 'Greetings in return',
        'add': 'Bot saves the new contact(can\'t be less than 10 digit)',
        'change': 'Bot saves the new phone number of the existing contact',
        'phone': 'Bot displays the phone number for the given name',
        'show all': 'Bot displays all saved contacts',
        'search': 'Bot displays the contact at your request',
        'write note': 'Bot writes a new note.',
        'good bye, close, exit': 'Bot completes its work',
        'help': 'Bot shows help info'}

help = ''
for key, value in commands_help.items():
    help += '{:<25} | {:<70}\n'.format(key, value)

class Bot:
    def __init__(self) -> None:
        self.file = 'contacts.json'
        self.book = AddressBook()
        self.notes = Notes()
        try:
            with open(self.file, 'rb') as f:
                contacts = pickle.load(f)
                self.book.data = contacts
        except:
            print('New AddressBook')

    @staticmethod
    def input_error(func):
        def inner(*args):
            try:
                return func(*args)
            except KeyError:
                return 'Contact not found'
            except ValueError:
                return f'Please follow the commands list \n{help}'
            except IndexError:
                return 'Please input command, name and/or phone'
        return inner

    def greeting(self, user_input):
        return "How can I help you?"

    @input_error
    def add(self, user_input):
        name, phone = user_input.lower().replace('add', '').split()
        record = Record(name, phone)

        for rec in self.book.data.values():
            if name in rec.name.value.lower():
                new_record = rec
                new_record.add_phone(phone)
                self.book.add_record(new_record)

        self.book.add_record(record)
        return 'New contact added!'
    
    def show_all(self, user_input):
        if not self.book.data:
            return 'You have no any contacts saved'
        
        return self.book
    
    def help(self, user_input):
        return help

    @input_error
    def change(self, user_input):
        name, phone, new_phone = user_input.lower().replace('change', '').split()

        for record in self.book.data.values():
            if name in record.name.value.lower():
                new_record = record
                new_record.edit_phone(phone, new_phone)
                self.book.add_record(new_record)
                return 'Contact updated!'
            
    @input_error
    def delete(self, user_input):
        name = user_input.lower().replace('delete', '')
        for record in self.book.data.values():
            if name == record.name.value.lower():         
                return self.book.delete(record)

    @input_error
    def phone(self, user_input):
        name = user_input.lower().replace('phone', '')
        return self.book.find(name)

    @input_error
    def write_note(self, user_input):
        note = user_input.replace('write', '').replace('note', '').lstrip()
        return self.notes.add_note(note)
             
    def exit(self, user_input):
        with open(self.file, 'wb') as f:
            pickle.dump(self.book.data, f)
        print('Good Bye')
        sys.exit()

    def search(self, user_input):
        text = user_input.lower().replace('search', '')
        s_text = text.strip().lower()
        result = []
        for record in self.book.data.values():
            if s_text in record.name.value.lower() + ' '.join([phone.value for phone in record.phones]):
                result.append(str(record))
        return result

    commands = {
            'hello': greeting,
            'add': add,
            'write note': write_note,
            'change': change,
            'phone': phone,
            'show all': show_all,
            'good bye': exit,
            'close': exit,
            'exit': exit,
            'search': search,
            'delete': delete,
            'help': help
            }

    @input_error
    def get_handler(self, user_input):
        for action in self.commands:
            if user_input.lower().startswith(action):
                return self.commands[action]

    def run(self):
        while True:
            user_input = input('>>')
            handler = self.get_handler(user_input)
            if handler == None:
                print('Unknown command! Please, enter command from the list below:\n')
                handler = self.get_handler('help') 
            result = handler(self, user_input)
            print(result)