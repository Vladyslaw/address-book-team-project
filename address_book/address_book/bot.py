import sys
import os
import pickle
from classes import AddressBook, Record, Phone, Birthday, Email
from notes import Notes
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from folder_sorter import sort_folder


def set_name():
    customer_input = input('    Input name: ')
    name = customer_input
    return name


def set_phone():
    customer_input = input('    Input phone: ')
    phone = Phone(customer_input)
    return str(phone)


def set_birthday():
    customer_input = input('    Input date of birthday (DD.MM.YYYY) or pass: ')
    birthday = Birthday(customer_input) if customer_input != 'pass' else None
    if birthday:
        return str(birthday)
    return birthday

def set_email():
    customer_input = input('    Input email or pass: ')
    email = Email(customer_input) if customer_input != 'pass' else None
    if email:
        return str(email)
    return email

def set_address():
    customer_input = input('    Input address or pass: ')
    address = customer_input if customer_input != 'pass' else None
    return address

  
class Bot:
    def __init__(self) -> None:
        self.contacts_file = 'contacts.bin'
        self.notes_file = 'notes.bin'
        self.book = AddressBook()
        self.notes = Notes()

        self.load_file(self.contacts_file, self.book, "AddressBook is created")
        self.load_file(self.notes_file, self.notes, "New NotesBook is created")
        
        self.commands = {
            'hello': self.greeting,
            'add': self.add,
            'change': self.change,
            'phone': self.phone,
            'show all': self.show_all,
            'good bye': self.exit,
            'close': self.exit,
            'exit': self.exit,
            'sort folder': self.folder_sort,
            'search phone': self.search_phone,
            'delete': self.delete,
            'help': self.help,
            'birthday': self.birthday,
            'write note': self.write_note,
            'search notes': self.search_notes,
            'remove note': self.remove_note,
            'edit note': self.edit_note,
            'create tag': self.create_tag,
            'link tag': self.link_tag,
            'show notes': self.show_notes
            }
        
        self.completer = self.set_compliter()

    def load_file(self, file_name, entity, message):
        try:
            with open(file_name, 'rb') as file:
                entity.data = pickle.load(file)
        except:
            print(message)

    def write_to_file(self, file_name, entity):
        with open(file_name, 'wb') as f:
            pickle.dump(entity.data, f)

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
        while True:
            name = set_name()
            if name:
                try:
                    phone = set_phone()
                except ValueError:
                    print('    Incorrect phone number, try again with 10 digit')
                    phone = set_phone()
            if phone:
                try:
                    birthday = set_birthday()
                except ValueError:
                    print('    Incorrect birthday format, try again with DD.MM.YYYY')
                    birthday = set_birthday()
            if birthday or birthday is None:
                try:
                    email = set_email()
                except ValueError:
                    print('    Incorrect email fotmat, try again with name@test.com')
                    email = set_email()
            if email or email is None:
                address = set_address()
            if address or address is None:
                break
        record = Record(name, phone, birthday, email, address)
        self.book.add_record(record)
        return 'New contact added!'
    
    def show_all(self, user_input):
        if not self.book.data:
            return 'You have no any contacts saved'
        
        return self.book
    
    def help(self, user_input):
        commands_help = {
        'hello': 'Greetings in return',
        'add': 'Bot saves the new contact(can\'t be less than 10 digit)',
        'change': 'Bot saves the new phone number of the existing contact',
        'phone': 'Bot displays the phone number for the given name',
        'show all': 'Bot displays all saved contacts',
        'search phone': 'Bot displays the contact at your request',
        'write note': 'Bot asks to input title and text',
        'edit note <title>': 'Bot edits note by title',
        'remove note <title>': 'Bot removed note by title',
        'good bye, close, exit': 'Bot completes its work',
        'help': 'Bot shows help info',
        'birthday': 'Bot shows nearest contacts birthday by given term (default 7 days)',
        'sort folder': 'Bot sorts the inqired folder'
        }

        help = ''
        for key, value in commands_help.items():
            help += '{:<25} | {:<70}\n'.format(key, value)
        return help

    @input_error
    def change(self, user_input):
        name, phone, new_phone = user_input.replace('change', '').split()

        for record in self.book.data.values():
            if name in record.name.value.lower():
                new_record = record
                new_record.edit_phone(phone, new_phone)
                self.book.add_record(new_record)
                return 'Contact updated!'
            
    @input_error
    def delete(self, user_input):
        name = user_input.replace('delete', '')
        for record in self.book.data.values():
            if name == record.name.value.lower():         
                return self.book.delete(record)

    @input_error
    def phone(self, user_input):
        name = user_input.replace('phone', '')
        return self.book.find(name)

    @input_error
    def write_note(self, user_input):
        if user_input != "write note":
            raise ValueError
        
        title = input('Please, input the title:\n')
        text = input('Please, input the text. You can leave this field empty:\n')

        return self.notes.add_note(title, text)
    
    @input_error
    def remove_note(self, user_input):
        note_to_remove = user_input.replace("remove note", '')

        return self.notes.delete_note(note_to_remove)
    
    @input_error
    def edit_note(self, user_input):
        note_to_edit = user_input.replace("edit note", '')
        text = input('Please, input the new note text.\n')

        return self.notes.edit_note(note_to_edit, text)
             
    def exit(self, user_input):
        if len(self.book.data) > 0:
            self.write_to_file(self.contacts_file, self.book)

        if len(self.notes.data) > 0:
            self.write_to_file(self.notes_file, self.notes)

        print('Good Bye')
        sys.exit()

    def search_phone(self, user_input):
        text = user_input.replace('search phone', '')
        s_text = text.strip().lower()
        result = []
        for record in self.book.data.values():
            if s_text in record.name.value.lower() + ' '.join([phone.value for phone in record.phones]):
                result.append(str(record))
        return result
    
    def folder_sort(self, user_input):
        target_folder_path = user_input.replace('sort folder ', '')
        if not os.path.exists(target_folder_path):
            return 'folder not found'
    
        return sort_folder(target_folder_path, display_analytics=True)

    @input_error
    def birthday(self, user_input, days=None):
        birthday_man = str()
        if days == None:
            days_depth = int(user_input.replace('birthday ', ''))
        else:
            days_depth = days
        
        days_depth = days_depth if days_depth != None else 7

        for record in self.book.data.values():
            try:
                if record.birthday.value:
                    if record.days_to_birthday(record.birthday) < days_depth:
                        birthday_man += '{:^15} {:^15}\n'.format(record.name.value, record.birthday.value)
            except AttributeError:
                continue
        
        if len(birthday_man) == 0 and days != None:
            return str()
        elif len(birthday_man) == 0:
            return f'\nNobody from your contacts celebrates birthday for the next {days_depth} days\n'
        elif days != None:
            birthday_man = f'Following contacts celebrate birthday in the nearest {days_depth} days:\n'\
                + '{:^15} {:^15}\n'.format('Name', 'Birthday') + birthday_man
            
        return birthday_man

    @input_error
    def search_notes(self, user_input: str) -> str:
        command_body = user_input.replace('search notes', '')
        command_body = command_body.strip().lower()
        
        return self.notes.find_notes(command_body).get_notes()

    @input_error
    def create_tag(self, user_input: str) -> str:
        command_body = user_input.replace('create tag', '')
        command_body = command_body.strip()

        return self.notes.tags.add_tag(command_body)
    
    @input_error
    def link_tag(self, user_input: str) -> str:
        if user_input != "link tag":
            raise ValueError
        
        note_title = input('Please, input the title of note you want to add:\n')
        tag_name = input('Please, input the name of tag you want to add:\n')

        return self.notes.add_tag_for_note(tag_name, note_title)
    
    def show_notes(self, user_input: str) -> str:
        if user_input != "show notes":
            raise ValueError
        
        return self.notes.get_notes()

    def set_compliter(self):
        function_names = list()
        for command in self.commands.keys():
            function_names.append(command)

        # function_names = ['hello', 'add', 'change', 'phone', 'show all', 'search phone', 'write note', 'help', 'exit']
        return WordCompleter(function_names)

    @input_error
    def get_handler(self, user_input):
        for action in self.commands:
            if user_input.startswith(action):
                return self.commands[action]

    def run(self):
        print('Hello!')
        print(self.birthday(str(), 30))

        while True:
            user_input = prompt('>> ', completer=self.completer).lower()
            handler = self.get_handler(user_input)
            if handler == None:
                print('Unknown command! Please, enter command from the list below:\n')
                handler = self.get_handler('help') 
            result = handler(user_input)
            print(result or '')