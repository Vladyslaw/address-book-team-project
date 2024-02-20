# Address Book Package

The Address Book package provides a command-line interface for managing contacts and notes efficiently. It allows users to add, edit, delete contacts, search for contacts by phone number, and perform various other operations related to contacts and notes.

## Features

- **Contact Management**: Add, edit, delete contacts with details like name, phone number, email, birthday, and address.
- **Notes Management**: Write, edit, delete notes with titles and text.
- **Tagging**: Tag notes for better organization and retrieval.
- **Search and Filter**: Search contacts by phone number, search notes by title or text, and find notes by tags.
- **Folder Sorting**: Sort files in a folder based on file extensions into predefined categories.

## Installation

1. Clone the repository:
git clone <repository_url>


2. Navigate to the address_book package directory:
cd address_book


3. Install dependencies:
pip install -r requirements.txt


## Usage

### Running the Application

To start the application, run the `run.py` script:
python run.py


### Commands

Once the application is running, you can interact with it using the following commands:

- **hello**: Greet the bot.
- **add**: Add a new contact to the address book.
- **phone**: Display the phone number for a given contact name.
- **show all**: Display all saved contacts.
- **good bye**, **close**, **exit**: Close the application.
- **help**: Display a list of available commands and their descriptions.
- **birthday**: Display contacts with birthdays within a specified number of days.
- **write note**: Write a new note.
- **edit note**: Edit an existing note by title.
- **remove note**: Remove a note by title.
- **search notes**: Search for notes by title or text.
- **create tag**: Create a new tag for organizing notes.
- **link tag**: Link a tag to a specific note.
- **show notes**: Display all saved notes.
- **find notes by tags**: Find notes associated with specific tags.
- **sort folder**: Sort files in a folder based on file extensions.

## File Structure

- **address_book/**
  - **bot.py**: Contains the main logic for the address book bot.
  - **classes.py**: Defines the classes for contacts and notes management.
  - **folder_sorter.py**: Implements functionality for sorting files in a folder.
  - **notes.py**: Handles operations related to notes, including tagging.
  - **run.py**: Entry point for running the address book application.
  - **\_\_init__.py**: Initializes the address book package.
  
## Contribution

Contributions to the Address Book package are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on the GitHub repository.

## License

This project is licensed under the MIT License.