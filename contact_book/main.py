"""This script implements a console assistant bot for managing contacts.
It supports adding, changing, and showing contacts, as well as managing birthdays.
All data is managed via AddressBook and Record classes.
New functionality includes birthday management and upcoming birthday queries.
"""

from models.record import Record
from models.addressbook import AddressBook
from storage import save_data, load_data
from views import ConsoleView, AbstractView

COMMANDS_DESCRIPTION = {
    "add [name] [phone]": "Add a new contact or phone to existing contact",
    "change [name] [old_phone] [new_phone]": "Change existing contact's phone",
    "phone [name]": "Show contact's phone number(s)",
    "all": "Show all contacts",
    "add-birthday [name] [DD.MM.YYYY]": "Add birthday to a contact in format DD.MM.YYYY",
    "show-birthday [name]": "Show birthday for a contact",
    "birthdays": "Show contacts with birthdays in the next 7 days (with greeting date, moved to Monday if on weekend)",
    "hello": "Greet the assistant",
    "help": "Show this help message",
    "exit/close": "Exit the program",
}


def input_error(func):
    """
    Decorator for handling errors in command handlers.
    Returns user-friendly error messages for common exceptions.
    """

    def wrapper(*args, **kwargs):
        view = args[-1]
        try:
            return func(*args, **kwargs)
        except IndexError:
            view.display_message("Error: Not enough arguments.")
        except KeyError:
            view.display_message("Error: Contact not found.")
        except ValueError as e:
            view.display_message(f"Error: {e}")
        return

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
        return "", []
    return parts[0].lower(), parts[1:]


@input_error
def add_contact(args, book: AddressBook, view: AbstractView) -> None:
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
    view.display_message(message)


@input_error
def change_contact(args, book: AddressBook, view: AbstractView) -> None:
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
        view.display_message("Error: Contact not found.")
        return
    record.edit_phone(old_phone, new_phone)
    view.display_message("Phone updated.")


@input_error
def show_phone(args, book: AddressBook, view: AbstractView) -> None:
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
        view.display_message("Error: Contact not found.")
        return
    if not record.phones:
        view.display_message("No phones for this contact.")
        return
    view.display_message(
        f"Phones for {name}: " + ", ".join(p.value for p in record.phones)
    )


def show_all_contacts(book: AddressBook, view: AbstractView) -> None:
    """
    Returns a string with all contacts.
    Args:
        book (AddressBook): AddressBook instance.
    Returns:
        str: List of all contacts.
    """
    view.display_all_contacts(book)


@input_error
def add_birthday(args, book: AddressBook, view: AbstractView) -> None:
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
        view.display_message("Error: Contact not found.")
        return
    record.add_birthday(birthday_str)
    view.display_message("Birthday added.")


@input_error
def show_birthday(args, book: AddressBook, view: AbstractView) -> None:
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
        view.display_message("Error: Contact not found.")
        return
    if record.birthday is None:
        view.display_message("No birthday for this contact.")
        return
    view.display_message(f"Birthday for {name}: {record.birthday}")


@input_error
def birthdays(_args, book: AddressBook, view: AbstractView) -> None:
    """
    Shows contacts with birthdays in the next 7 days.
    """
    upcoming = book.get_upcoming_birthdays()
    view.display_upcoming_birthdays(upcoming)


def print_help(view: AbstractView):
    """
    Prints the help message with all supported commands using the view.
    """
    view.display_help(COMMANDS_DESCRIPTION)


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
