"""This script implements a console assistant bot for managing contacts.
It supports adding, changing, and showing contacts, as well as managing birthdays.
All data is managed via AddressBook and Record classes.
New functionality includes birthday management and upcoming birthday queries.
"""

from models.record import Record
from models.addressbook import AddressBook
from storage import save_data, load_data

def input_error(func):
    """
    Decorator for handling errors in command handlers.
    Returns user-friendly error messages for common exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Error: Not enough arguments."
        except KeyError:
            return "Error: Contact not found."
        except ValueError as e:
            return f"Error: {e}"
    return wrapper

def parse_input(user_input: str) -> tuple:
    """
    Parses user input into command and arguments.
    Args:
        user_input (str): input string from user.
    Returns:
        tuple: (command, args)
    """
    parts = user_input.strip().split()
    if not parts:
        return '', []
    return parts[0].lower(), parts[1:]

@input_error
def add_contact(args, book: AddressBook) -> str:
    """
    Adds a new contact or phone to existing contact.
    Args:
        args (list): [name, phone]
        book (AddressBook): AddressBook instance.
    Returns:
        str: Success or error message.
    """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook) -> str:
    """
    Changes existing contact's phone number.
    Args:
        args (list): [name, old_phone, new_phone]
        book (AddressBook): AddressBook instance.
    Returns:
        str: Success message or error if contact/phone not found.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."

@input_error
def show_phone(args, book: AddressBook) -> str:
    """
    Shows phone numbers for a contact.
    Args:
        args (list): [name]
        book (AddressBook): AddressBook instance.
    Returns:
        str: Phone numbers or not found message.
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if not record.phones:
        return "No phones for this contact."
    return f"Phones for {name}: " + ', '.join(p.value for p in record.phones)

def show_all_contacts(book: AddressBook) -> str:
    """
    Returns a string with all contacts.
    Args:
        book (AddressBook): AddressBook instance.
    Returns:
        str: List of all contacts.
    """
    return str(book)

@input_error
def add_birthday(args, book: AddressBook) -> str:
    """
    Adds a birthday to a contact.
    Args:
        args (list): [name, birthday_str]
        book (AddressBook): AddressBook instance.
    Returns:
        str: Success or error message.
    """
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday_str)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook) -> str:
    """
    Shows birthday for a contact.
    Args:
        args (list): [name]
        book (AddressBook): AddressBook instance.
    Returns:
        str: Birthday or not found message.
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.birthday is None:
        return "No birthday for this contact."
    return f"Birthday for {name}: {record.birthday}"

@input_error
def birthdays(_args, book: AddressBook) -> str:
    """
    Shows contacts with birthdays in the next 7 days.
    Args:
        args (list): not used
        book (AddressBook): AddressBook instance.
    Returns:
        str: List of contacts with upcoming birthdays.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    result = []
    for item in upcoming:
        result.append(f"{item['name']}: birthday {item['birthday']}, greet on {item['greet_date']}")
    return "\n".join(result)

def print_help():
    """
    Prints the help message with all supported commands.
    """
    print(
        "Commands:\n"
        "add username phone - Add a new contact or phone to existing contact\n"
        "change username old_phone new_phone - Change existing contact's phone\n"
        "phone username - Show contact's phone number(s)\n"
        "all - Show all contacts\n"
        "add-birthday username DD.MM.YYYY - Add birthday to a contact in format DD.MM.YYYY\n"
        "show-birthday username - Show birthday for a contact\n"
        "birthdays - Show contacts with birthdays in the next 7 days (with greeting date, moved to Monday if on weekend)\n"
        "hello - Greet the assistant\n"
        "help - Show this help message\n"
        "exit or close - Exit the program"
    )

def main():
    """
    Main loop of the contact assistant.
    Handles user input and command execution.
    Loads AddressBook from disk at startup and saves it at exit.
    """
    book = load_data()
    print("Welcome to the contact assistant!")
    print("Type 'help' for commands, 'exit' or 'close' to quit.")

    while True:
        user_input = input(">>> ").strip()
        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["exit", "close"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "help":
            print_help()

        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
