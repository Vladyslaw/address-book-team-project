import sys
import os
import pickle
import re
from classes import AddressBook, Record, Phone, Birthday, Email
from notes import Notes
from folder_sorter import sort_folder


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


def set_name():
    customer_input = input('    Input name: ')
    name = customer_input
    return name


def set_phone():
    customer_input = input('    Input phone: ')
    phone = Phone(customer_input)
    return str(phone)


def set_birthday():
    customer_input = input('    Input date of birthday or pass: ')
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
        self.file = 'contacts.json'
        self.book = AddressBook()
        self.notes = Notes()
        try:
            with open(self.file, 'rb') as file:
                self.book.data = pickle.load(file)
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
        with open(self.file, 'wb') as f:
            pickle.dump(self.book.data, f)
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

    def birthday(self, user_input):
        s = '\n'
        indx = user_input.replace('birthday', '')

        if not indx:
            indx = 7
        
        for record in self.book.data.values():
            try:
                if record.birthday.value:
                    if record.days_to_birthday(record.birthday) < int(indx):
                        s += '{:^15} {:^15}\n'.format(record.name.value, record.birthday.value)
            except AttributeError:
                continue
        return s if s != '\n' else '\nNobody has selebrate birthday on this term\n'

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

    commands = {
            'hello': greeting,
            'add': add,
            'change': change,
            'phone': phone,
            'show all': show_all,
            'good bye': exit,
            'close': exit,
            'exit': exit,
            'sort folder': folder_sort,
            'search phone': search_phone,
            'delete': delete,
            'help': help,
            'birthday': birthday,
            'write note': write_note,
            'search notes': search_notes,
            'remove note': remove_note,
            'edit note': edit_note,
            'create tag': create_tag,
            'link tag': link_tag,
            'show notes': show_notes
            }

    @input_error
    def get_handler(self, user_input):
        for action in self.commands:
            if user_input.startswith(action):
                return self.commands[action]

    def run(self):
        while True:
            user_input = input('>>').lower().strip()
            handler = self.get_handler(user_input)
            if handler == None:
                print('Unknown command! Please, enter command from the list below:\n')
                handler = self.get_handler('help') 
            result = handler(self, user_input)
            print(result or '')
