import sys
import pickle
from classes import AddressBook, Record, Phone, Birthday, Email
import re
commands_help = {
        'hello': 'Greetings in return',
        'add': 'Bot saves the new contact(can\'t be less than 10 digit)',
        'change': 'Bot saves the new phone number of the existing contact',
        'phone': 'Bot displays the phone number for the given name',
        'show all': 'Bot displays all saved contacts',
        'search': 'Bot displays the contact at your request',
        'good bye, close, exit': 'Bot completes its work',
        'help': 'Bot shows help info'}

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
    customer_input = input('    Input email: ')
    email = Email(customer_input) if customer_input != 'pass' else None
    if email:
        return str(email)
    return email

class Bot:
    def __init__(self) -> None:
        self.file = 'contacts.json'
        self.book = AddressBook()
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
        # line = user_input.lower().replace('add', '').split()
        # name = line[0] if len(line) > 0 else None
        # phone = line[1] if len(line) > 1 else None
        # birthday = line[2] if len(line) > 2 else None
        # email = line[3] if len(line) > 3 else None
        # record = Record(name, phone, birthday, email)
       
        # name, phone, birthday, email = user_input.replace('add', '').split()
        # record = Record(name, phone, birthday, email)

        # for rec in self.book.data.values():
        #     if name in rec.name.value.lower():
        #         new_record = rec
        #         new_record.add_phone(phone)
        #         self.book.add_record(new_record)
        # while True:
        #     customer_input = input('Input name: ')
        #     name = customer_input
        #     if name:
        #         customer_input = input('input phone number: ')
        #         phone = customer_input
        #     if phone:
        #         customer_input = input('Input date of birthday or pass: ')
        #         birthday = customer_input if customer_input != 'pass' else None
        #     if birthday or birthday is None:
        #         pattern = '[a-zA-Z]{1}[a-zA-Z0-9._]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,}'
        #         customer_input = input('Input a user email or pass: ')
        #         matching = re.fullmatch(pattern, customer_input)
        #         if matching and customer_input != 'pass':
        #             email = customer_input if customer_input != 'pass' else None
        #         customer_input = input('Input a user email or pass: ')                  
        #     if email or email is None:
        #         break

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
                    print(' Incorrect email fotmat, try again with name@test.com')
                    email = set_email()
            if email or email is None:
                break
        record = Record(name, phone, birthday, email)

        line = user_input.replace('add', '').split()
        name = line[0] if len(line) > 0 else None
        phone = line[1] if len(line) > 1 else None
        birthday = line[2] if len(line) > 2 else None
        record = Record(name, phone, birthday, email)

        # for rec in self.book.data.values():
        #     if name in rec.name.value.lower():
        #         new_record = rec
        #         new_record.add_phone(phone)
        #         self.book.add_record(new_record)

        record = Record(name, phone, birthday, email)
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
             
    def exit(self, user_input):
        with open(self.file, 'wb') as f:
            pickle.dump(self.book.data, f)
        print('Good Bye')
        sys.exit()

    def search(self, user_input):
        text = user_input.replace('search', '')
        s_text = text.strip().lower()
        result = []
        for record in self.book.data.values():
            if s_text in record.name.value.lower() + ' '.join([phone.value for phone in record.phones]):
                result.append(str(record))
        return result

    commands = {
            'hello': greeting,
            'add': add,
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
            if user_input.startswith(action):
                return self.commands[action]

    def run(self):
        while True:
            user_input = input('>>').lower()
            handler = self.get_handler(user_input)
            if handler == None:
                print('Unknown command! Please, enter command from the list below:\n')
                handler = self.get_handler('help') 
            result = handler(self, user_input)
            print(result)