"""This module provides functions for saving and loading the AddressBook
using pickle serialization to persist data between sessions.
"""

import pickle

# Assuming AddressBook is imported correctly from its path
from models.addressbook import AddressBook

# Constant with an explicitly defined path to the data file inside the contact_book folder
DEFAULT_FILENAME = "contact_book/addressbook.pkl"


def save_data(book: AddressBook, filename: str = DEFAULT_FILENAME):
    """
    Serializes and saves the AddressBook instance to a file using pickle.
    Args:
        book (AddressBook): The AddressBook instance to save.
        filename (str): The file path for saving (defaults to DEFAULT_FILENAME).
    """
    # 'wb' - write binary. Creates or overwrites the file at the specified path.
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = DEFAULT_FILENAME) -> AddressBook:
    """
    Loads and deserializes the AddressBook instance from a file using pickle.
    Args:
        filename (str): The file path for loading (defaults to DEFAULT_FILENAME).

    Returns:
        AddressBook: The loaded AddressBook instance or a new one if the file is not found.
    """
    try:
        # 'rb' - read binary. Attempts to read the data.
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # If the file does not exist, return a new, empty AddressBook instance
        return AddressBook()
