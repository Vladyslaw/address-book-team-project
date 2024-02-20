import sys
import os
import pickle
from classes import AddressBook, Record, Phone, Birthday, Email, Address
from notes import Notes
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from folder_sorter import sort_folder


def input_birthday():
    birthday = input('    Input date of birthday: ')
    return Birthday(birthday)


def input_email():
    email = input('    Input email: ')
    return Email(email)


def input_address():
    address = input('    Input address: ')
    return Address(address)

  
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
            'phone': self.phone,
            'show-all': self.show_all,
            'good-bye': self.exit,
            'close': self.exit,
            'exit': self.exit,
            'sort-folder': self.folder_sort,
            'search-phone': self.search_phone,
            'delete': self.delete,
            'help': self.help,
            'birthday': self.birthday,
            'write note': self.write_note,
            'search notes': self.search_notes,
            'remove note': self.remove_note,
            'edit note': self.edit_note,
            'create tag': self.create_tag,
            'link tag': self.link_tag,
            'show notes': self.show_notes,
            'find notes by tags': self.search_notes_by_tags,
            'edit-phone': self.edit_phone,
            'edit-birthday': self.edit_birthday,
            'edit-email': self.edit_email,
            'edit-address': self.edit_address
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
                return 'Please input command and name'
        return inner

    def greeting(self):
        return "How can I help you?"

    def get_record(self, name):
        for record in self.book.data.values():
            if record.name.value == name:
                return record
        
        return None
    
    @input_error
    def get_record_by_name_input(self):
        name = input('\tEnter contact name: ').rstrip().lstrip()
        record_to_change = get_record(name)
        while record_to_change == None:
            print(f'There is no such contact with name {name}')
            name = input('\tEnter contact name: ').rstrip().lstrip()
            record_to_change = get_record(name)
        
        return record_to_change
    
    @input_error
    def name_input(self):
        return input('\tEnter name: ')

    @input_error
    def phone_input(self):
        phone_input = input('\tEnter phone: ')
        phone = Phone(phone_input)
        while not phone.is_valid():
            print('\tInvalid phone number format! Phone must contain 10 digits.')
            phone_input = input('\tEnter phone: ')
        
        return phone
    
    @input_error
    def birhtday_input(self):
        birthday_input = input('\tEnter date of birthday (DD.MM.YYYY) or pass: ')
        birthday = 'Not set'
        if birthday_input not in ('pass', ''):
            birthday = Birthday(birthday_input)
            while not birthday.is_valid() and birthday_input not in ('pass', ''):
                print('\tIncorrect birthday format, try again with DD.MM.YYYY')
                birthday_input = input('\tEnter date of birthday (DD.MM.YYYY) or pass: ')
        
        return birthday
    
    @input_error
    def email_input(self):
        email_input = input('\tEnter email or pass: ')
        email = 'Not set'
        if email_input not in ('pass', ''):
            email = Email(email_input)
            while not email.is_valid() and email_input not in ('pass', ''):
                print('\tIncorrect email format, try again in format name@test.com')
                email_input = input('\tEnter or pass: ')
        
        return email

    @input_error
    def address_input(self):
        address = input('\tEnter address or pass: ')
        if address in ('pass', ''):
            address = 'Not set'
        
        return address

    @input_error
    def add(self):
        name = self.name_input()
        phone = self.phone_input()
        birthday = self.birhtday_input()
        email = self.email_input()
        address = self.address_input()
        
        record = Record(name, phone, birthday, email, address)
        self.book.add_record(record)
        return 'New contact was added!'
    
    def show_all(self):
        if not self.book.data:
            return 'You have no any contacts saved'
        
        return self.book
    
    def help(self):
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
    def edit_phone(self):
        record_to_change = self.get_record_by_name_input()
        phone = self.phone_input()

        record_to_change.change_phone(phone, str(new_phone))
        self.book.add_record(record_to_change)
        return '\tContact updated!' 

    @input_error
    def edit_birthday(self):
        record_to_change = self.get_record_by_name_input()
        birthday = self.birhtday_input()
        record_to_change.change_birthday(str(birthday))
        self.book.add_record(record_to_change)
        return 'Contact updated!'
            
    @input_error
    def edit_email(self):
        record_to_change = self.get_record_by_name_input()
        email = self.email_input()
        record_to_change.change_email(str(email))
        self.book.add_record(record_to_change)
        return 'Contact updated!'
          
    @input_error
    def edit_address(self):
        record_to_change = self.get_record_by_name_input()
        address = self.address_input()
        record_to_change.change_address(str(address))
        self.book.add_record(record_to_change)
        return 'Contact updated!'
       
    @input_error
    def delete(self):
        record_to_delete = self.get_record_by_name_input()
        return self.book.delete(record_to_delete)

    @input_error
    def phone(self):
        name = self.name_input()
        return self.book.find(name)

    @input_error
    def write_note(self):
        title = input('Please, enter the title: ')
        text = input('Please, enter the text. You can leave this field empty: ')
        return self.notes.add_note(title, text)
    
    @input_error
    def remove_note(self):
        note_to_remove = input('Please, enter the title of the note: ')
        return self.notes.delete_note(note_to_remove)
    
    @input_error
    def edit_note(self):
        note_to_edit = input('Please, enter the title of the note: ')
        text = input('Please, enter the new text for the note: ')

        return self.notes.edit_note(note_to_edit, text)
             
    def exit(self):
        if len(self.book.data) > 0:
            self.write_to_file(self.contacts_file, self.book)

        if len(self.notes.data) > 0:
            self.write_to_file(self.notes_file, self.notes)

        print('Good Bye')
        sys.exit()

    def search_phone(self):
        phone_to_search = self.phone_input()
        result = []
        for record in self.book.data.values():
            if phone_to_search in record.name.value + ' '.join([phone.value for phone in record.phones]):
                result.append(str(record))
        return result
    
    @input_error
    def search_notes_by_tags(self):
        tag_name = input('Please, enter the tag name: ')
        tag_id = self.notes.get_tag_id(tag_name)
        if tag_id == None:
            return f"There is no such tag {tag_name}"

        return self.notes.find_notes_by_tag(tag_id=tag_id)
    
    def folder_sort(self):
        target_folder_path = input('Please, enter the path to folder: ')
        if not os.path.exists(target_folder_path):
            return 'folder not found'
    
        return sort_folder(target_folder_path, display_analytics=True)

    @input_error
    def birthday(self, days=None):
        birthday_man = str()
        if days == None:
            days_depth = int(input('Please, enter the depth in days: '))
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
            birthday_man = f"Contacts below celebrate birthday soon. Don't forget to prepare a gift and congrat them ;)\n"\
                + '{:^15} {:^15}\n'.format('Name', 'Birthday') + birthday_man
            
        return birthday_man

    @input_error
    def search_notes(self) -> str:
        note_to_search = input('Please, enter the title of the note: ').strip().lower()
        return self.notes.find_notes(note_to_search).get_notes()

    @input_error
    def create_tag(self) -> str:
        tag = input('Please, enter the title of the tag: ').strip()
        return self.notes.tags.add_tag(tag)
    
    @input_error
    def link_tag(self) -> str:
        note_title = input('Please, input the title of note you want to add: ')
        tag_name = input('Please, input the name of tag you want to add: ')
        return self.notes.add_tag_for_note(tag_name, note_title)
    
    def show_notes(self) -> str:
        return self.notes.get_notes()

    def set_compliter(self):
        function_names = list()
        for command in self.commands.keys():
            function_names.append(command)

        # function_names = ['hello', 'add', 'change', 'phone', 'show all', 'search phone', 'write note', 'help', 'exit']
        return WordCompleter(function_names)

    @input_error
    def get_handler(self, user_input):
        user_command = user_input.lower().rstrip().lstrip()
        return self.commands.get(user_command)

    def run(self):
        print('Hello!')
        print(self.birthday(30))

        while True:
            user_input = prompt('>> ', completer=self.completer)
            handler = self.get_handler(user_input)
            if handler == None:
                print('Unknown command! Please, enter command from the list below:\n')
                handler = self.get_handler('help') 
            result = handler()
            print(result or '')